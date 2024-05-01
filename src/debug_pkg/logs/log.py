import logging 
from contextlib import contextmanager
import time
import constans_pkg.constans as constans

# megkéne oldani hogy jól adja át a z infot a futo processben 


@contextmanager
def timed():
    start_time = time.time()
    yield
    end_time = time.time()
    print("Total execution time: \033[31;1;4m{}\033[0m sec".format(end_time - start_time))



logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s] %(levelname)s: %(message)s" 
if constans.DEV_MODE:
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logging.basicConfig(format=FORMAT, level=logging.INFO)


def log(message="no message added"):
    return logger.debug(message)


if __name__ == "__main__":
    log()
    timed()
