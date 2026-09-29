from openfreebuds import APP_ROOT

ASSETS_PATH = APP_ROOT / "openfreebuds_qt" / "assets"
I18N_PATH = APP_ROOT / "openfreebuds_qt" / "assets" / "i18n"

IGNORED_LOG_TAGS = [
    "qasync._QEventLoop",
    "qasync.QThreadExecutor",
    "qasync._QThreadWorker",
    "qasync._windows._EventWorker",
    "PIL.PngImagePlugin",
]

LINK_WEBSITE = "https://github.com/librebuds/librebuds-windows"
LINK_WEBSITE_HELP = "https://github.com/librebuds/librebuds-windows"
LINK_GITHUB = "https://github.com/librebuds/librebuds-windows"
LINK_RPC_HELP = "https://github.com/librebuds/librebuds-windows#remote-control"

WIN32_BODY_STYLE = """
QPushButton, 
QComboBox, 
QComboBox QAbstractItemView:item, 
QTreeView::item { 
    padding: 6px 12px; 
}

QLineEdit {
    padding: 4px 8px;
}
"""
