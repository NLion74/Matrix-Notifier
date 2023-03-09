import config
import logging
import coverage

logger = logging.getLogger(__name__)


class coverage_handler:
    def __int__(self):
        self.cov =  coverage.Coverage()

    def start(self):
        if config.coverage:
            logger.info("Start coverage engine")
            self.cov.start()

    def save(self):
        if config.coverage:
            logger.info("Saving coverage files")
            self.cov.stop()
            self.cov.save()
