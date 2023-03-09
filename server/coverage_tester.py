from coverage import Coverage

import config
import logging
from time import time
import os

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

            if not os.path.exists(f"{config.datadir_server}/coverage"):
                os.mkdir(f"{config.datadir_server}/coverage")

            self.cov.stop()
            self.cov.save()
