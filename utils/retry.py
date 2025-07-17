import asyncio
import functools
import httpx
from utils.logger import log_error, get_logger

logger = get_logger(__name__)

def retry_async(max_retries: int = 3, delay: float = 2.0):
    """
    Asynchroner Retry-Decorator für coroutine-Funktionen.
    Führt Wiederholungsversuche nur bei transienten Fehlern durch (z.B. Netzwerkprobleme oder 5xx Server-Fehler).
    Andere Fehler (z.B. 4xx Client-Fehler) werden sofort weitergereicht.

    :param max_retries: Maximale Anzahl der Versuche.
    :param delay: Verzögerung zwischen den Versuchen in Sekunden.
    """

    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(
                "retry_async kann nur auf async-Funktionen angewendet werden"
            )

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (httpx.ConnectError, httpx.TimeoutException) as e:
                    # Transient network errors
                    last_exc = e
                    logger.warning(
                        f"Versuch {attempt}/{max_retries}: Netzwerkfehler bei '{func.__name__}': {e}"
                    )
                    if attempt == max_retries:
                        break
                    await asyncio.sleep(delay)
                except httpx.HTTPStatusError as e:
                    # Retry on 5xx server errors, fail immediately on 4xx client errors
                    if 500 <= e.response.status_code < 600:
                        last_exc = e
                        logger.warning(
                            f"Versuch {attempt}/{max_retries}: Serverfehler ({e.response.status_code}) bei '{func.__name__}': {e}"
                        )
                        if attempt == max_retries:
                            break
                        await asyncio.sleep(delay)
                    else:
                        # Non-retriable client error (4xx), re-raise immediately
                        logger.error(
                            f"Nicht wiederholbarer Client-Fehler ({e.response.status_code}) bei '{func.__name__}'. Breche ab."
                        )
                        raise

            log_error(
                f"Alle {max_retries} Retries für '{func.__name__}' fehlgeschlagen. Letzter Fehler: {last_exc}"
            )
            raise last_exc

        return wrapper

    return decorator