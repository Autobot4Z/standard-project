import logging
import google.cloud.logging
from config import (
    DEBUG_LEVEL,
    GOOGLE_CLOUD_PROJECT,
    CLOUD_LOG_NAME,
    CLOUD_ERROR_LOG_NAME,
)

# Map string level names to logging constants
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Get the logging level constant, default to INFO if invalid
        level = LOG_LEVELS.get(DEBUG_LEVEL.upper(), logging.INFO)
        logger.setLevel(level)
    return logger


_cloud_logging_client = None
_cloud_log_handler_for_deletions = None
_cloud_log_handler_for_errors = None
fallback_logger = get_logger("cloud_logging_fallback")


def _initialize_cloud_logging():
    """
    Initialisiert den Google Cloud Logging Client und den Handler
    für spezifische Lösch-Logs.
    Diese Funktion stellt sicher, dass der Client nur einmal initialisiert wird.
    """
    global \
        _cloud_logging_client, \
        _cloud_log_handler_for_deletions, \
        _cloud_log_handler_for_errors
    if _cloud_logging_client is None:
        try:
            _cloud_logging_client = google.cloud.logging.Client(
                project=GOOGLE_CLOUD_PROJECT
            )
            _cloud_log_handler_for_deletions = _cloud_logging_client.logger(
                CLOUD_LOG_NAME
            )
            _cloud_log_handler_for_errors = _cloud_logging_client.logger(
                CLOUD_ERROR_LOG_NAME
            )
            logging.getLogger(__name__).info(
                "Cloud Logging Client für Löschereignisse und Error Handling initialisiert."
            )
        except Exception as e:
            logging.getLogger(__name__).error(
                f"Fehler beim Initialisieren des Cloud Logging Clients: {e}"
            )
            _cloud_logging_client = None
            _cloud_log_handler_for_deletions = None
            _cloud_log_handler_for_errors = None

def cloud_log_deletion_event(message, severity="INFO", **kwargs):
    """
    Sendet eine spezifische Lösch-Log-Nachricht an Google Cloud Logging.
    Diese Logs werden unter dem Namen 'data-deletion-events' in Cloud Logging
    gespeichert und können von einer Senke in einen spezifischen Bucket exportiert werden.
    """
    # Sicherstellen, dass Cloud Logging initialisiert ist
    if _cloud_logging_client is None:
        _initialize_cloud_logging()

    if _cloud_log_handler_for_deletions:
        severity_map = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        cloud_severity = severity_map.get(severity.upper(), "INFO")

        # Verwenden Sie log_struct, um zusätzliche Daten (kwargs) als JSON-Payload zu senden
        # Dies ist nützlich für die Analyse in Cloud Logging
        payload = {"message": message}
        payload.update(kwargs)  # Fügt alle zusätzlichen Schlüsselwortargumente hinzu

        _cloud_log_handler_for_deletions.log_struct(payload, severity=cloud_severity)
    else:
        # Fallback, wenn Cloud Logging nicht initialisiert werden konnte
        # oder ein Fehler auftrat. Verwenden Sie den Standard-Logger hier.
        # Es ist wichtig, auch diese Fälle zu protokollieren.
        fallback_logger.error(
            f"Cloud Logging Handler nicht verfügbar. Konnte Lösch-Log nicht an Cloud senden: {message}"
        )


def cloud_log(message, severity="ERROR", **kwargs):
    """
    Sendet eine spezifische Error-Log-Nachricht an Google Cloud Logging.
    """
    # Sicherstellen, dass Cloud Logging initialisiert ist
    if _cloud_logging_client is None:
        _initialize_cloud_logging()

    if _cloud_log_handler_for_errors:
        severity_map = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
        }
        cloud_severity = severity_map.get(severity.upper(), "ERROR")

        # Verwenden Sie log_struct, um zusätzliche Daten (kwargs) als JSON-Payload zu senden
        # Dies ist nützlich für die Analyse in Cloud Logging
        payload = {"message": message}
        payload.update(kwargs)  # Fügt alle zusätzlichen Schlüsselwortargumente hinzu

        _cloud_log_handler_for_errors.log_struct(payload, severity=cloud_severity)
    else:
        # Fallback, wenn Cloud Logging nicht initialisiert werden konnte
        # oder ein Fehler auftrat. Verwenden Sie den Standard-Logger hier.
        # Es ist wichtig, auch diese Fälle zu protokollieren.
        fallback_logger.error(
            f"Cloud Logging Handler nicht verfügbar. Konnte Error Log nicht an Cloud senden: {message}"
        )
