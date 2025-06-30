from google.cloud import tasks_v2
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from services.firestore_service import FirestoreService
from utils.logger import get_logger, log_error, log_deletion_event
from config import (
    GOOGLE_CREDENTIALS_PATH,
    CLOUD_TASKS_LOCATION,
    CLOUD_TASKS_QUEUE,
    GOOGLE_CLOUD_PROJECT,
    CLOUD_TASKS_MAX_RETRIES,
)
import uvicorn

logger = get_logger("main.py")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        tasks_client = tasks_v2.CloudTasksClient().from_service_account_file(
            GOOGLE_CREDENTIALS_PATH
        )
        logger.debug("Cloud Tasks Client erfolgreich authentifiziert.")
    except Exception as e:
        log_error(
            f"Fehler beim authentifizieren des Cloud Tasks Client: {e}", "CRITICAL"
        )

    app.state.tasks_client = tasks_client
    app.state.firestore_service = FirestoreService()

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/webhook/new_invoice")
async def new_invoice(request: Request):
    client = app.state.tasks_client
    firestore_service = app.state.firestore_service

    task_name = request.headers.get("X-CloudTasks-TaskName")
    retry_count = int(request.headers.get("X-CloudTasks-TaskRetryCount", "0"))

    logger.info(
        f"Neue Task {task_name} empfangen. Retry: {retry_count}. Programm wird gestartet."
    )

    if not task_name:
        # kein Task-Header → nicht von Cloud Tasks aufgerufen
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Ungültiges JSON")

    event_id = payload[0].get("eventId", "")

    if not event_id:
        raise HTTPException(status_code=400, detail="Ungültiges Event ID")

    # tasks_client.task_path erstellt den vollständigen Pfad
    full_task_name = client.task_path(
        GOOGLE_CLOUD_PROJECT, CLOUD_TASKS_LOCATION, CLOUD_TASKS_QUEUE, task_name
    )

    # Idempotency Prüfung
    if not await firestore_service.check_and_set_webhook(event_id):
        await delete_task(full_task_name)
        return {"status": "duplicate", "message": "Webhook already processed."}

    try:
        # Hauptlogik ausführen
        pass

    except Exception as e:
        # Bei fehlerhafter Ausführung wird Webhook auf Idempotency Collection gelöscht.
        await firestore_service.delete_webhook(event_id)

        # Bei erreichen der maximale Anzahl an Retries wird die Google Task gelöscht.
        if retry_count >= CLOUD_TASKS_MAX_RETRIES:
            await delete_task(full_task_name, success=False)
        raise HTTPException(status_code=400, detail=f"Fehler bei Verarbeitung: {e}")

    # Wenn die Verarbeitung erfolgreich war, löschen Sie die Aufgabe.
    await delete_task(full_task_name)

    await firestore_service.set_webhook_status(event_id)

    return {"status": "success", "task_name": full_task_name}
    

async def delete_task(task_name: str, success: bool = True):
    """
    Löschen von Cloud Task bei erfolgreicher oder fehlerhafter Verarbeitung.
    Extra Error Log senden bei fehlerhafter Verarbeitung.
    """
    client = app.state.tasks_client
    try:
        client.delete_task(name=task_name)
        log_deletion_event(f"Google Task {task_name} erfolgreich gelöscht.", "INFO")
        if not success:
            log_error(
                f"Google Task {task_name} gelöscht ohne erfolgreiche Ausführung.",
                "CRITICAL",
            )
    except Exception as e:
        log_deletion_event(
            f"Fehler beim Löschen der Google Task {task_name}: {e}", "ERROR"
        )
        log_error(f"Fehler beim Löschen der Google Task {task_name}: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
