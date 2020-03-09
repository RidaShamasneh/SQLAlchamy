from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMenu, QDialogButtonBox, QVBoxLayout, QScrollArea, QWidget, QFrame, QLayout, QHBoxLayout


class CustomQMenu(QMenu):
    ok_cancel_dialog_button_rejected = QtCore.pyqtSignal()
    ok_cancel_dialog_button_accepted = QtCore.pyqtSignal()

    def __init__(self):
        super(CustomQMenu, self).__init__()
        self._ok_cancel_dialog_button = None

    def _setup_ui(self):
        self._main_vertical_layout = QVBoxLayout()
        self._main_vertical_layout.setContentsMargins(0, 0, 0, 0)  # (int left, int top, int right, int bottom)
        self._main_vertical_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self._main_vertical_layout)
        self._scroll_area = QScrollArea()
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.NoFrame)
        self._main_vertical_layout.addWidget(self._scroll_area)
        self.__scroll_widget = QWidget()
        self._scroll_layout = QVBoxLayout()
        self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_layout.setSpacing(0)
        self._scroll_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.__scroll_widget.setLayout(self._scroll_layout)
        self._scroll_area.setWidget(self.__scroll_widget)
        self._footer_horizontal_layout = QHBoxLayout()
        self._main_vertical_layout.addLayout(self._footer_horizontal_layout)

    def _create_menu(self):
        # construct QdialogButtonBox
        self._ok_cancel_dialog_button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                                         QtCore.Qt.Horizontal, self)
        self._ok_cancel_dialog_button.rejected.connect(lambda: self.ok_cancel_dialog_button_rejected.emit())
        self._ok_cancel_dialog_button.accepted.connect(lambda: self.ok_cancel_dialog_button_accepted.emit())
        # Add QdialogButtonBox to filter_menu
        self._footer_horizontal_layout.addWidget(self._ok_cancel_dialog_button, 0, Qt.AlignRight)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Close:
            self.ok_cancel_dialog_button_rejected.emit()
            return True
        return False