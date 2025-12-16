import os

# Gunicorn config variables
loglevel = os.environ.get("LOG_LEVEL", "info")
workers = int(os.environ.get("GUNICORN_PROCESSES", "2"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# For debugging and testing
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": True},
        "gunicorn.error": {"level": "INFO"},
        "gunicorn.access": {"level": "INFO"},
    },
}
