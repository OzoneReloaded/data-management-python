import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from sql_auth_handler import connect_to_database

# что это такое


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.textHost = QLineEdit(self)
        self.textDatabase = QLineEdit(self)
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)

        self.host_label = QLabel("Host:")
        self.database_label = QLabel("Database:")
        self.login_label = QLabel("Login:")
        self.password_label = QLabel("Password:")

        self.buttonLogin = QPushButton('Embark', self)
        self.buttonLogin.clicked.connect(self.embark)

        layout = QVBoxLayout(self)
        layout.addWidget(self.host_label)
        layout.addWidget(self.textHost)
        layout.addWidget(self.database_label)
        layout.addWidget(self.textDatabase)
        layout.addWidget(self.login_label)
        layout.addWidget(self.textName)
        layout.addWidget(self.password_label)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def embark(self):
        """ функция вызывает жесть и кровищу """
        try:
            self.connection = connect_to_database(self.textHost.text(), self.textName.text(), self.textDatabase.text(), self.textPass.text())
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('flow')
        self.setWindowIcon(QIcon('flow.ico'))
        self.mainLayout = QGridLayout()
        self.mainLayout.setRowStretch(0, 6)
        self.mainLayout.setRowStretch(1, 4)

        self.create_status_group()
        self.create_query_buttons()
        self.create_query_field()
        self.create_database_table()
        self.setLayout(self.mainLayout)

    def create_status_group(self):
        pixmap = QPixmap('flow.jpg').scaledToWidth(100)
        icon = QLabel()
        icon.setPixmap(pixmap)

        test = 'test'

        database_info_group = QGroupBox("Status:")
        database_info_list = QVBoxLayout()

        host_info = QLabel(f"Host: {test}")
        database_info = QLabel(f"Database: {test}")
        user_info = QLabel(f"User: {test}")

        database_info_list.addWidget(icon)
        database_info_list.addWidget(host_info)
        database_info_list.addWidget(database_info)
        database_info_list.addWidget(user_info)
        database_info_group.setLayout(database_info_list)
        self.mainLayout.addWidget(database_info_group, 0, 1)

    def create_database_table(self):
        tableWidget = QTableWidget(10, 10)
        self.mainLayout.addWidget(tableWidget, 0, 0)

    def create_query_field(self):
        sql_query_group = QGroupBox("SQL Query:")
        sql_query_window = QVBoxLayout()
        sql_query_field = QTextEdit()
        sql_query_field.setPlaceholderText("Let the thought flow..")
        sql_query_window.addWidget(sql_query_field)
        sql_query_group.setLayout(sql_query_window)
        self.mainLayout.addWidget(sql_query_group, 1, 0)

    def create_query_buttons(self):
        execute_query_button = QPushButton("Execute", self)
        clear_query_button = QPushButton("Clear", self)
        execute_query_button.clicked.connect(self.execute_sql)
        clear_query_button.clicked.connect(self.execute_sql)
        query_button_group = QGroupBox("Query commands:")
        query_buttons = QVBoxLayout()
        query_buttons.addWidget(execute_query_button)
        query_buttons.addWidget(clear_query_button)
        query_button_group.setLayout(query_buttons)
        self.mainLayout.addWidget(query_button_group, 1, 1)

    def execute_sql(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()

    if login.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
