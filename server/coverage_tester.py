import config
import logging
import coverage

logger = logging.getLogger(__name__)


class CoverageHandler:
    def __int__(self):
        cov = coverage.Coverage()
        self.cov = cov

    def start(self):
        if config.coverage:
            logger.info("Start coverage engine")
            self.cov.start()

    def save(self):
        if config.coverage:
            logger.info("Saving coverage files")
            self.cov.stop()
            self.cov.save()
