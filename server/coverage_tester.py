from coverage import Coverage

import config
import logging
from time import time

logger = logging.getLogger(__name__)


class CoverageHandler:
    def __init__(self):
        if config.coverage:
            coveragedatafile = ".coverage-" + str(int(time()))
            self.cov = Coverage(data_file=f"{config.datadir_server}/{coveragedatafile}")

    def start(self):
        if config.coverage:
            logger.info("Start coverage engine")
            self.cov.start()

    def save(self):
        if config.coverage:
            logger.info("Saving coverage files")
            self.cov.stop()
            self.cov.save()
