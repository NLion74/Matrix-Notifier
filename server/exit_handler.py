import logging
import signal

import config

logger = logging.getLogger(__name__)


class Exit:
    def __init__(self, cov):
        self.cov = cov
        signal.signal(signal.SIGTERM, self.exit_cleanly)
        signal.signal(signal.SIGINT, self.exit_cleanly)
        signal.signal(signal.SIGABRT, self.exit_cleanly)

    def exit_cleanly(self, signal_number, stackframe):
        logger.info("Received exit signal. Exiting...")
        if config.coverage:
            logger.info("Saving coverage files")

            try:
                self.cov.stop()
                self.cov.save()
                logger.info("Successfully saved coverage")
            except Exception as e:
                logger.critical("Exception occurred while saving coverage:")
                logger.critical(e)

        quit(0)
