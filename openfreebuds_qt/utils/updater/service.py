from PyQt6.QtWidgets import QWidget

from openfreebuds.utils.logger import create_logger
from openfreebuds_qt.config import OfbQtConfigParser

# LibreBuds: updates come from GitHub releases; the upstream update server is not used.
UpdateCheckerConfig = None
MmkUpdaterQt = None

log = create_logger("OfbQtUpdaterService")


class OfbQtUpdaterService:
    def __init__(self, parent: QWidget):
        self.config = OfbQtConfigParser.get_instance()
        self.updater_config = None
        self.updater = None

    async def boot(self):
        # LibreBuds: updates come from GitHub releases; the upstream update server is not used.
        log.info("Skip, disabled")
        return

    async def check_now(self):
        # LibreBuds: updates come from GitHub releases; the upstream update server is not used.
        return
