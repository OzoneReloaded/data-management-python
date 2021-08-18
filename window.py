import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from sql_auth_handler import DatabaseHandler

# что это такое

database_instance = None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def set_default_window_options(current_window: QDialog):
    icon_path = resource_path('flow.ico')
    current_window.setWindowTitle('flow')
    current_window.setWindowIcon(QIcon(icon_path))


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        set_default_window_options(self)

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
            global database_instance
            database_instance = DatabaseHandler(self.textHost.text(),
                                                self.textName.text(),
                                                self.textDatabase.text(),
                                                self.textPass.text())
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


class MainWindow(QDialog):
    """ how do i insert emoji here?? """
    def __init__(self, database, parent=None):
        super(MainWindow, self).__init__(parent)

        set_default_window_options(self)

        self.database = database

        self.tableWidget = None
        self.query_field = None
        self.last_received_data = None

        self.mainLayout = QGridLayout()
        self.mainLayout.setRowStretch(0, 6)
        self.mainLayout.setRowStretch(1, 4)

        self.create_status_group()
        self.create_query_buttons()
        self.create_database_table()
        self.create_query_field()
        self.setLayout(self.mainLayout)

    def create_status_group(self):
        pixmap = QPixmap('flow.jpg').scaledToWidth(100)
        icon = QLabel()
        icon.setPixmap(pixmap)

        database_info_group = QGroupBox("Status:")
        database_info_list = QVBoxLayout()

        host_info = QLabel(f"Host: {self.database.host}")
        database_info = QLabel(f"Database: {self.database.database}")
        user_info = QLabel(f"User: {self.database.user}")

        database_info_list.addWidget(icon)
        database_info_list.addWidget(host_info)
        database_info_list.addWidget(database_info)
        database_info_list.addWidget(user_info)
        database_info_group.setLayout(database_info_list)
        self.mainLayout.addWidget(database_info_group, 0, 1)

    def create_database_table(self):
        self.tableWidget = QTableWidget(10, 10)
        self.tableWidget.setRowCount(0)
        self.mainLayout.addWidget(self.tableWidget, 0, 0)

    def create_query_field(self):
        sql_query_group = QGroupBox("SQL Query:")
        sql_query_window = QVBoxLayout()
        # I feel sorry for this
        self.query_field = QTextEdit()
        self.query_field.setPlaceholderText("Let the thought flow..")
        sql_query_window.addWidget(self.query_field)
        sql_query_group.setLayout(sql_query_window)
        self.mainLayout.addWidget(sql_query_group, 1, 0)
        # Not sorry anymore

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
        query_string = self.query_field.toPlainText()
        cursor = database_instance.cursor
        connection = database_instance.connection
        try:
            cursor.execute(query_string)
            self.last_received_data = cursor.fetchall()
            connection.commit()
            self.draw_received_data_to_table()
        except Exception as e:
            connection.rollback()
            QMessageBox.warning(self, 'SQL Query error', str(e))

    def draw_received_data_to_table(self):
        self.tableWidget.setRowCount(0)
        """ draw_received_data_from_the_database_and_place_it_to_the_table_in_this_window_to_display_it(self): """
        if not self.last_received_data:
            QMessageBox.warning(self, 'Warning', 'No data received from database. Check your SQL Query.')
            return 0
        else:
            for row_number, row_data in enumerate(self.last_received_data):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            # for row_number, row_data in enumerate(self.last_received_data):
            #     self.tableWidget.insertRow(row_number)
            #
            #     for column_number, data in enumerate(row_data):
            #         self.tableWidget.setItem(row_number,
            #                                  column_number, QTableWidgetItem(str(data)))
            # return 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()

    if login.exec_() == QDialog.Accepted:
        window = MainWindow(database_instance)
        window.show()
        sys.exit(app.exec_())
