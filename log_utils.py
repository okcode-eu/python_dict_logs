import logging, logging.config
import copy
import os, pathlib


class MyStyle(object):
    default_format = '%(message)s'
    asctime_format = '%(asctime)s'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format

    def usesTime(self):
        return True

    def format(self, record):
        # Sometimes MyLogger will not be used. For example when Python itself
        # raises an 'Task exception was never retrieved' error.
        if not hasattr(record, "shortpath"):
            record.shortpath = ".." + os.sep.join(pathlib.PurePath(record.pathname).parts[-2:])
        return self._fmt % record.__dict__


class MyFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        fmt = kwargs.pop("fmt", "%(message)s")
        super().__init__(*args, fmt=fmt, **kwargs)

    def format(self, record):
        out = super().format(record)
        if record.extras:
            # Have fun here, use json.dumps or whatever suits you.
            out += " # %s" % str(record.extras)
        return out


class MyFilter(logging.Filter):
    def filter(self, record):
        # Add anything to extras on every call.
        record.extras['sth'] = "ohoho"
        return True


class MyLogger(logging.Logger):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        if extra is not None:
            extra_dict = copy.copy(extra)  # just in case
        else:
            extra_dict = {}
        record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        record.extras = extra_dict
        return record


def configure_logging():
    logging._STYLES['p'] = (MyStyle, logging.BASIC_FORMAT)
    logging.setLoggerClass(MyLogger)
    LOGFILE_PATH = 'some_path'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'my': {
                '()': MyFilter,
            }
        },
        'formatters': {
            'console': {
                '()': MyFormatter,
                'fmt': "%(levelname)s %(shortpath)s:%(funcName)s:%(lineno)s %(message)s",
                "style": "p",
            },
        },
        'handlers': {
            'console':{
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'filters': ['my'],
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
    logging.config.dictConfig(LOGGING)


if __name__ == "__main__":
    configure_logging()
    log = logging.getLogger(__name__)
    log.info("Some error", extra={'d': 'abc'})
