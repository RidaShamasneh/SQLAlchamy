from PyQt4.QtGui import QMessageBox


class CBMessageBoxes(object):
    WARNING = QMessageBox.Warning
    CRITICAL = QMessageBox.Critical
    INFO = QMessageBox.Information

    NO = QMessageBox.No
    YES = QMessageBox.Yes

    @staticmethod
    def popup_message(icon, title, text, detailed_text=None, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        if detailed_text:
            msg.setDetailedText(detailed_text)
        # needed to make close button enabled
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setEscapeButton(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def prompt_user(icon, title, text, parent=None):
        msg = QMessageBox(parent)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_()
