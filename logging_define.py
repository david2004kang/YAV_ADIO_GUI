#!"C:\Python27\python.exe"
# -*- coding: utf-8 -*-
import logging
import os
import datetime

_path = '{}\\report'.format(os.getcwd())
if not os.path.isdir(_path):
    os.system("mkdir " + _path)
log_file_name = datetime.datetime.now().strftime(_path + "\\debug_log_%Y%m%d.txt")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(message)s',
                    filename=log_file_name)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger('').addHandler(console)


def logger(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            logging.debug('<< %s <<' % fn.__name__)
            out = apply(fn, args, kwargs)
            logging.debug('>> %s >>' % fn.__name__)
            # Return the return value
            return out
        except Exception as _logger_exception:
            logging.debug('exception: %s' % fn.__name__)
            logging.exception(_logger_exception)

    return wrapper


def protect(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return apply(fn, args, kwargs)
        except Exception as _logger_exception:
            logging.debug('exception: %s' % fn.__name__)
            logging.exception(_logger_exception)

    return wrapper
