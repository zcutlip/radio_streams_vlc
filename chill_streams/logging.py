import logging.config
import logging

_log_level = logging.INFO


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] [%(name)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'propagate': True,
            'handlers': ['console'],
        },
    },
}

logging.config.dictConfig(LOGGING)


def enable_debug_logging():
    global _log_level
    _log_level = logging.DEBUG


def get_logger(logname):
    logger = logging.getLogger(logname)
    # logger.propagate = True

    logger.setLevel(_log_level)
    return logger
