from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStackedWidget, QLabel, QLineEdit, QFormLayout
)
import hotel
from PySide6.QtCore import Qt

class AddWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Добавить записи")
        self.setMinimumSize(600, 400)
        self.db = db

        # Главное окно с кнопками выбора таблиц и центральной областью
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Виджет переключения форм
        self.form_stack = QStackedWidget()

        # Кнопки выбора таблицы
        self.client_button = QPushButton("Добавить Клиента")
        self.client_button.clicked.connect(lambda: self.change_form(0))
        self.room_button = QPushButton("Добавить Номер")
        self.room_button.clicked.connect(lambda: self.change_form(1))
        self.service_button = QPushButton("Добавить Услугу")
        self.service_button.clicked.connect(lambda: self.change_form(2))

        # Компоновка боковой панели
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.addWidget(self.client_button)
        self.sidebar_layout.addWidget(self.room_button)
        self.sidebar_layout.addWidget(self.service_button)

        # Формы для заполнения
        self.client_form = self.create_client_form()
        self.room_form = self.create_room_form()
        self.service_form = self.create_service_form()

        # Добавляем формы в стек
        self.form_stack.addWidget(self.client_form)
        self.form_stack.addWidget(self.room_form)
        self.form_stack.addWidget(self.service_form)

        # Главная компоновка
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.sidebar_layout)
        self.main_layout.addWidget(self.form_stack)

        self.central_widget.setLayout(self.main_layout)

    def change_form(self, index):
        """Переключение между формами"""
        self.form_stack.setCurrentIndex(index)

    def create_client_form(self):
        """Форма для добавления клиента"""
        form_layout = QFormLayout()

        self.client_last_name = QLineEdit()
        self.client_first_name = QLineEdit()
        self.client_middle_name = QLineEdit()
        self.client_gender = QLineEdit()
        self.client_birth_date = QLineEdit()
        self.client_phone = QLineEdit()

        form_layout.addRow("Фамилия:", self.client_last_name)
        form_layout.addRow("Имя:", self.client_first_name)
        form_layout.addRow("Отчество:", self.client_middle_name)
        form_layout.addRow("Пол:", self.client_gender)
        form_layout.addRow("Дата рождения:", self.client_birth_date)
        form_layout.addRow("Телефон:", self.client_phone)

        submit_button = QPushButton("Добавить")
        submit_button.clicked.connect(self.add_client)
        form_layout.addRow(submit_button)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def create_room_form(self):
        """Форма для добавления номера"""
        form_layout = QFormLayout()

        self.room_name = QLineEdit()
        self.room_description = QLineEdit()
        self.room_price = QLineEdit()

        form_layout.addRow("Название:", self.room_name)
        form_layout.addRow("Описание:", self.room_description)
        form_layout.addRow("Цена:", self.room_price)

        submit_button = QPushButton("Добавить")
        submit_button.clicked.connect(self.add_room)
        form_layout.addRow(submit_button)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def create_service_form(self):
        """Форма для добавления услуги"""
        form_layout = QFormLayout()

        self.service_name = QLineEdit()
        self.service_description = QLineEdit()
        self.service_price = QLineEdit()

        form_layout.addRow("Название:", self.service_name)
        form_layout.addRow("Описание:", self.service_description)
        form_layout.addRow("Цена:", self.service_price)

        submit_button = QPushButton("Добавить")
        submit_button.clicked.connect(self.add_service)
        form_layout.addRow(submit_button)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        return form_widget

    def add_client(self):
        pass
    #    try:
    #         last_name = self.client_last_name
    #         first_name = self.client_first_name
    #         middle_name = self.client_middle_name
    #         gender = self.client_gender
    #         birth_date = self.client_birth_date
    #         phone = self.client_phone
    #    except Exception as e:
    #        self.db.rollback()
    #        return
    #    try:
    #        new_client = hotel.Guest(
    #            last_name = last_name,
    #            first_name = first_name,
    #            middle_name = middle_name,
    #            gender = 
    #        )

    def add_room(self):
        """Добавление номера (заглушка)"""
        print("Добавлен номер:", self.room_name.text())

    def add_service(self):
        """Добавление услуги (заглушка)"""
        print("Добавлена услуга:", self.service_name.text())
