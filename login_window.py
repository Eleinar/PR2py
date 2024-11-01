from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
from main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setWindowTitle("Вход")
        self.login = QLineEdit()
        self.login.setPlaceholderText("login")
        self.base = QLineEdit()
        self.base.setPlaceholderText("base")
        self.login_button = QPushButton()
        self.login_button.setText("Подключиться к базе")

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.login)
        self.hlayout.addWidget(self.base)
        self.hlayout.addWidget(self.login_button)

        self.setLayout(self.hlayout)
        self.login_button.clicked.connect(self.onClickLogin)
        
        
    def onClickLogin(self):
        login = self.login.text()
        base = self.base.text()
        self.mainwindow = MainWindow(login, base)
        self.mainwindow.show()
        self.close()