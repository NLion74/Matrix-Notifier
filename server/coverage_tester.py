from coverage import Coverage

import config
import logging
from time import time

logger = logging.getLogger(__name__)


class CoverageHandler:
    def __init__(self):
        if config.coverage:
            coveragedatafile = ".coverage-" + str(int(time()))
            self.cov = Coverage(data_file=f"{config.datadir_server}/coverage/{coveragedatafile}")

    def start(self):
        if config.coverage:
            logger.info("Started coverage engine")

            self.cov.start()

    def save(self):
        if config.coverage:
            logger.info("Saving coverage files")

            try:
                self.cov.stop()
                self.cov.save()
                logger.info("Successfully saved coverage")
            except Exception as e:
                logger.critical("Exception occurred while saving coverage:")
                logger.critical(e)
            finally:
                quit(0)
