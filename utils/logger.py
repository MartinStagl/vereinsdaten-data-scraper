from os.path import exists, join
from os import mkdir
import logging
import datetime

def initLogger():
    log_path = './log'
    if not exists(log_path):
        mkdir(log_path)

    logging.basicConfig(
        filename=join(log_path, 'data-scraper' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.log'),format='%(asctime)s - %(name)s - %(funcName)s - %(filename)s - %(threadName)s - %(levelname)s - %(message)s')
    # create logger
    logger = logging.getLogger('data-scraper')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(filename)s - %(threadName)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger