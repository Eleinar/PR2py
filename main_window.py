from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QMessageBox)
import hotel
from sqlalchemy import func, or_
from add_window import AddWindow

class MainWindow(QMainWindow):
    def __init__(self, login=None, base=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Гостиница")
        self.setMinimumSize(900, 300)
        self.db = hotel.create_connection(login, base)
        self.current_table = None

        # Кнопки интерфейса
        self.client_button = QPushButton("Клиенты")
        self.client_button.clicked.connect(self.onClickClient)
        
        self.room_button = QPushButton("Номерной фонд")
        self.room_button.clicked.connect(self.onClickRoom)
        
        self.service_button = QPushButton("Доп.Услуги")
        self.service_button.clicked.connect(self.onClickService)
        
        self.booking_button = QPushButton("Бронирования")
        self.booking_button.clicked.connect(self.onClickBooking)

        self.add_button = QPushButton("Добавить записи")
        self.add_button.clicked.connect(self.onClickAdd)
        
        self.delete_button = QPushButton("Удалить запись")  # Кнопка удаления
        self.delete_button.clicked.connect(self.onClickDelete)

        # Поле ввода и фильтры
        self.line_find = QLineEdit()
        self.line_find.setPlaceholderText("Поиск по значению")
        self.combobox = QComboBox()
        self.gender_list = []
        self.room_list = []
        self.getListFilter()

        # Компоновка
        self.v_button_layout = QVBoxLayout()
        self.v_button_layout.addWidget(self.client_button)
        self.v_button_layout.addWidget(self.room_button)
        self.v_button_layout.addWidget(self.service_button)
        self.v_button_layout.addWidget(self.booking_button)
        self.v_button_layout.addWidget(self.add_button)
        self.v_button_layout.addWidget(self.delete_button)
        self.v_button_layout.addWidget(self.line_find)
        self.v_button_layout.addWidget(self.combobox)

        self.table = QTableWidget()
        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.v_button_layout)
        self.hlayout.addWidget(self.table)
        
        self.widget = QWidget()
        self.widget.setLayout(self.hlayout)
        self.setCentralWidget(self.widget)

    # Получаем список для фильтра
    def getListFilter(self):
        genders = self.db.query(hotel.Gender).all()
        rooms = self.db.query(hotel.Room).all()
        
        self.gender_list = ["Любой"] + [gender.gender_name for gender in genders]
        self.room_list = ["Любой"] + [room.name for room in rooms]

    # Применяем фильтры
    def applyClientFilters(self):
        last_name_filter = self.line_find.text()
        selected_gender = self.combobox.currentText()
        clients = self.getClients(last_name_filter, selected_gender)
        
        self.table.clear()
        self.table.setRowCount(len(clients))
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Место рождения", "Паспорт", "Телефон"])

        for i, c in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(str(c.id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(c.last_name)))
            self.table.setItem(i, 2, QTableWidgetItem(str(c.first_name)))
            self.table.setItem(i, 3, QTableWidgetItem(str(c.middle_name)))
            self.table.setItem(i, 4, QTableWidgetItem(str(c.gender_str.gender_name)))
            self.table.setItem(i, 5, QTableWidgetItem(str(c.birth_date)))
            self.table.setItem(i, 6, QTableWidgetItem(str(c.birth_place)))
            self.table.setItem(i, 7, QTableWidgetItem(f"{c.passport_str.passport_series} {c.passport_str.passport_number}"))
            self.table.setItem(i, 8, QTableWidgetItem(str(c.phone)))

    def onClickClient(self):
        self.current_table = "clients"
        self.line_find.setPlaceholderText("Поиск по фамилии")
        self.combobox.clear()
        self.combobox.addItems(self.gender_list)
        self.line_find.textChanged.connect(self.applyClientFilters)
        self.combobox.currentTextChanged.connect(self.applyClientFilters)
        self.applyClientFilters()
    
    def getClients(self, last_name_filter=None, gender_filter=None):
        query = self.db.query(hotel.Guest).join(hotel.Gender, hotel.Guest.gender_id == hotel.Gender.id)
        
        if last_name_filter:
            query = query.filter(hotel.Guest.last_name.like(f"%{last_name_filter}%"))
        
        if gender_filter and gender_filter != "Любой":
            query = query.filter(hotel.Gender.gender_name == gender_filter)

        return query.all()

    def onClickRoom(self):
        self.line_find.setPlaceholderText("Поиск по названию номера")
        self.combobox.clear()
        self.line_find.textChanged.connect(self.applyRoomFilters)
        self.combobox.currentTextChanged.connect(self.applyRoomFilters)
        self.applyRoomFilters()

    def applyRoomFilters(self):
        room_name_filter = self.line_find.text()
        selected_room = self.combobox.currentText()
        rooms = self.getRooms(room_name_filter if selected_room == "Любой" else selected_room)

        self.table.clear()
        self.table.setRowCount(len(rooms))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена"])

        for i, r in enumerate(rooms):
            self.table.setItem(i, 0, QTableWidgetItem(str(r.id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(r.name)))
            self.table.setItem(i, 2, QTableWidgetItem(str(r.description)))
            self.table.setItem(i, 3, QTableWidgetItem(str(r.price)))

    def getRooms(self, room_filter=None):
        query = self.db.query(hotel.Room)
        if room_filter and room_filter != "Любой":
            query = query.filter(hotel.Room.name.like(f"%{room_filter}%"))
        return query.all()

    def onClickService(self):
        self.current_table = "services"
        self.line_find.setPlaceholderText("описание услуги")
        self.line_find.textChanged.connect(self.applyServiceFilters)
        self.combobox.clear()
        self.applyServiceFilters()

    def applyServiceFilters(self):
        service_filter = self.line_find.text()
        services = self.getService(service_filter)

        self.table.clear()
        self.table.setRowCount(len(services))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена"])

        for i, s in enumerate(services):
            self.table.setItem(i, 0, QTableWidgetItem(str(s.id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(s.name)))
            self.table.setItem(i, 2, QTableWidgetItem(str(s.description)))
            self.table.setItem(i, 3, QTableWidgetItem(str(s.price)))

    def getService(self, text=None):
        query = self.db.query(hotel.Services)
        if text:
            query = query.filter(hotel.Services.description.like(f"%{text}%"))
        return query.all()

    def onClickBooking(self):
        self.line_find.setPlaceholderText("Поиск по фамилии или названию комнаты")
        self.combobox.clear()
        self.combobox.addItems(self.room_list)
        self.line_find.textChanged.connect(self.applyBookingFilters)
        self.combobox.currentTextChanged.connect(self.applyBookingFilters)
        self.applyBookingFilters()

    def applyBookingFilters(self):
        room_filter = self.combobox.currentText()
        search_text = self.line_find.text()
        bookings = self.getBookings(room_filter, search_text)

        self.table.clear()
        self.table.setRowCount(len(bookings))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Гость", "Срок проживания", "Комната", "Прибытие", "Отбытие", "Скидка"])

        for i, b in enumerate(bookings):
            self.table.setItem(i, 0, QTableWidgetItem(str(b.id)))
            self.table.setItem(i, 1, QTableWidgetItem(f"{b.guest_str.last_name} {b.guest_str.first_name} {b.guest_str.middle_name}"))
            self.table.setItem(i, 2, QTableWidgetItem(str(b.stay_until)))
            self.table.setItem(i, 3, QTableWidgetItem(str(b.room_str.name)))
            self.table.setItem(i, 4, QTableWidgetItem(str(b.arrival)))
            self.table.setItem(i, 5, QTableWidgetItem(str(b.departure)))
            self.table.setItem(i, 6, QTableWidgetItem(str(b.discount)))

    def getBookings(self, room_filter=None, search_text=None):
        query = self.db.query(hotel.Questionnaire)

        if room_filter and room_filter != "Любой":
            query = query.filter(hotel.Questionnaire.room_str.name == room_filter)

        if search_text:
            query = query.filter(
                or_(
                    hotel.Questionnaire.room_str.name.like(f"%{search_text}%"),
                    hotel.Questionnaire.guest_str.last_name.like(f"%{search_text}%")
                )
            )

        return query.all()

    def onClickAdd(self):
        self.add_window = AddWindow()
        self.add_window.show()
        
    def onClickDelete(self):
        # Проверка текущей таблицы
        if self.current_table not in ["clients", "services"]:
            QMessageBox.warning(self, "Удаление", "Удаление доступно только для клиентов или услуг.")
            return

        # Получить текущую выбранную строку
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Удаление", "Выберите запись для удаления.")
            return

        # Получить ID записи
        record_id = self.table.item(selected_row, 0).text()
        if not record_id:
            QMessageBox.warning(self, "Удаление", "Не удалось определить ID записи.")
            return

        # Удалить запись
        if self.current_table == "clients":
            self.deleteClient(record_id)
        elif self.current_table == "services":
            self.deleteService(record_id)

        # Уведомить пользователя
        QMessageBox.information(self, "Удаление", f"Запись с ID {record_id} успешно удалена.")
        # Обновить таблицу
        if self.current_table == "clients":
            self.applyClientFilters()
        elif self.current_table == "services":
            self.applyServiceFilters()

    def deleteClient(self, client_id):
        try:
            # Находим связанные записи в Questionnaire
            questionnaires = self.db.query(hotel.Questionnaire.id).filter(
                hotel.Questionnaire.guest == client_id
            ).all()
            questionnaire_ids = [q.id for q in questionnaires]
    
            if questionnaire_ids:
                # Удаление записей из Services_in_questionnaire по найденным Questionnaire IDs
                self.db.query(hotel.Services_in_questionnaire).filter(
                    hotel.Services_in_questionnaire.questionnaire_id.in_(questionnaire_ids)
                ).delete(synchronize_session="fetch")
    
                # Удаление записей из Questionnaire
                self.db.query(hotel.Questionnaire).filter(
                    hotel.Questionnaire.id.in_(questionnaire_ids)
                ).delete(synchronize_session="fetch")
    
            # Удаление записи из Guest
            self.db.query(hotel.Guest).filter(hotel.Guest.id == client_id).delete()
    
            # Применение изменений
            self.db.commit()
    
            # Уведомление пользователя об успехе
            QMessageBox.information(self, "Успех", "Клиент и связанные данные успешно удалены.")
            # Обновление таблицы клиентов
            self.applyClientFilters()
    
        except Exception as e:
            # Откат изменений в случае ошибки
            self.db.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить клиента: {e}")


    def deleteService(self, service_id):
        try:
        # Удаление связанных записей
            self.db.query(hotel.Services_in_questionnaire).filter(hotel.Services_in_questionnaire.service_id == service_id).delete()
        # Удаление самой услуги
            self.db.query(hotel.Services).filter(hotel.Services.id == service_id).delete()
            self.db.commit()
        except Exception as e:
            self.db.rollback()  # Откат изменений в случае ошибки
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить услугу: {e}")


    def closeEvent(self, event):
        self.db.close_all()
        print("Соединение закрыто")
