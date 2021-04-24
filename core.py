import sys
import sql_auth_handler

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow
from auth_window import Ui_AuthDialog


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class AuthDialog(QDialog, Ui_AuthDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def draw_auth(self):
        auth_dialog = AuthDialog(self)
        auth_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_on_start_dialog = AuthDialog()
    auth_on_start_dialog.draw_auth()
    print(auth_on_start_dialog.password.text())
    sys.exit(app.exec())
