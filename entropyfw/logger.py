import logging
from logging.handlers import RotatingFileHandler

log = logging.getLogger('entropyfw')
log.setLevel(logging.DEBUG)

nh = logging.NullHandler()
log.addHandler(nh)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def add_file_handler(file_path='/var/log/entropyfw.log', level=logging.DEBUG):
    global log
    global formatter
    fh = RotatingFileHandler(filename=file_path, maxBytes=1024*1024, backupCount=5)
    fh.setLevel(level=level)
    # create formatter and add it to the handlers
    fh.setFormatter(formatter)
    log.addHandler(fh)
