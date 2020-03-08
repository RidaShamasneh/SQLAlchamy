from PyQt4.QtGui import QWidget, QVBoxLayout, QToolBar


class GenericTabWidget(QWidget):
    _TOOLBAR_STYLE = "QToolBar {border: solid white; padding: 8px 8px 8px 8px};"

    def __init__(self, main_window=None):
        super(GenericTabWidget, self).__init__(None)
        self._main_window = main_window
        self._main_layout = QVBoxLayout(self)
        self._toolbar = QToolBar(self)
        self._toolbar.setStyleSheet(self._TOOLBAR_STYLE)
        self._main_layout.setMenuBar(self._toolbar)
        self.setLayout(self._main_layout)
