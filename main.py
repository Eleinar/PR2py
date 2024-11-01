from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from login_window import LoginWindow, MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()