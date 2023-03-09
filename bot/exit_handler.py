import logging

import config

logger = logging.getLogger(__name__)


class Exit:
    def __init__(self, cov):
        self.cov = cov

    def exit_cleanly(self, signal_number, stackframe):
        logger.info("Received exit signal. Exiting...")
        if config.coverage:
            self.cov.save()
        quit(0)
