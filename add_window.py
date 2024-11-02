from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from main_window import MainWindow
import hotel
from sqlalchemy import func, or_

class AddWindow(QWidget):
    def __init__(self):
        super().__init__()

    def createClientsUI(self):

        self.layout = QVBoxLayout()

        self.id_label = QLabel("ID")
        self.
