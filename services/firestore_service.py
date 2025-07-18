from google.cloud.exceptions import Conflict
import asyncio
from google.cloud import firestore
from utils.logger import get_logger, cloud_log
from config import GOOGLE_CREDENTIALS_PATH, IDEMPOTENCY_COLLECTION
import hashlib

logger = get_logger("firestore_service.py")


class FirestoreService:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._collection = IDEMPOTENCY_COLLECTION
        try:
            self._db = firestore.Client().from_service_account_json(
                GOOGLE_CREDENTIALS_PATH
            )
            logger.debug("Firestore Client erfolgreich initialisiert.")
        except Exception as e:
            cloud_log(
                f"Fehler beim initialisieren des Firestore Client: {str(e)}", "CRITICAL"
            )

    async def check_and_set_webhook(self, id: str) -> bool:
        """
        Prüft in einer atomaren Transaktion, ob der Webhook bereits verarbeitet wird/wurde.
        Gibt True zurück, wenn die Verarbeitung fortgesetzt werden soll.
        Gibt False zurück, wenn der Webhook ein Duplikat ist.
        """
        id = str(id)
        
        async with self._lock:
            hashed_id = await self._hash_id(id)
            doc_ref = self._db.collection(self._collection).document(hashed_id)

            try:
                # Versuche das Dokument zu erstellen (atomic operation)
                doc_ref.create(
                    {"status": "PROCESSING", "timestamp": firestore.SERVER_TIMESTAMP}
                )
                logger.debug(f"Webhook {id} auf PROCESSING gesetzt")
                return True
            except Conflict:
                # Dokument existiert bereits (Conflict)
                logger.debug(
                    f"Doppelter Webhook erkannt: {id}. Verarbeitung wird übersprungen."
                )
                return False
            except Exception as e:
                cloud_log(f"Unerwarteter Fehler bei Id {id}: {e}")
                return False

    async def set_webhook_status(self, id: str):
        """
        Setzt nach Beendigung der Webhookverarbeitung den Status des Firestore Eintrags auf COMPLETED.
        Verhindert zukünftige doppelte Ausführungen.
        """
        id = str(id)
        
        try:
            hashed_id = await self._hash_id(id)
            doc_ref = self._db.collection(self._collection).document(hashed_id)
            doc_ref.update({"status": "COMPLETED"})
        except Exception as e:
            cloud_log(f"Fehler beim aktualisieren der ID {id} in Firestore: {e}")

    async def delete_webhook(self, id: str):
        """
        Webhook aus Firestore löschen.
        """
        id = str(id)
        
        try:
            hashed_id = await self._hash_id(id)
            doc_ref = self._db.collection(self._collection).document(hashed_id)
            doc_ref.delete()
        except Exception as e:
            cloud_log(f"Fehler beim löschen der ID {id} in Firestore: {e}")

    async def _hash_id(self, id: str) -> bytes:
        str_id = str(id)
        return hashlib.sha256(str_id.encode()).hexdigest()
