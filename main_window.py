
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QWidget,
QVBoxLayout, QHBoxLayout, QPushButton,QTableWidget, QTableWidgetItem,
QLineEdit, QComboBox)
import hotel
from sqlalchemy import func

        

class MainWindow (QMainWindow):
    def __init__(self, login, base):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Гостинница")
        self.setMinimumSize(900,300)
        self.db = hotel.create_connection(login, base)
        self.client_button = QPushButton()
        self.client_button.setText("Клиенты")
        self.client_button.clicked.connect(self.onClickClient)
        self.room_button = QPushButton()
        self.room_button.setText("Номерной фонд")
        self.room_button.clicked.connect(self.onClickRoom)
        self.service_button = QPushButton()
        self.service_button.setText("Доп.Услуги")
        self.service_button.clicked.connect(self.onClickService)
        self.booking_button = QPushButton()
        self.booking_button.setText("Бронирования")
        self.booking_button.clicked.connect(self.onClickBooking)
        
        
        self.line_find = QLineEdit()
        self.line_find.setPlaceholderText("Поиск по значению")
        
        
        self.combobox = QComboBox()
        self.gender_list = []
        self.room_list = []
        self.getListFilter()
        
        
        self.v_button_layout = QVBoxLayout()
        
        self.v_button_layout.addWidget(self.client_button)
        self.v_button_layout.addWidget(self.room_button)
        self.v_button_layout.addWidget(self.service_button)
        self.v_button_layout.addWidget(self.booking_button)
        self.v_button_layout.addWidget(self.line_find)
        
        self.v_button_layout.addWidget(self.combobox)
        
        self.v_button_layout.addStretch(5) # Эта функция отвечает за пространство между элементами
        
        self.table = QTableWidget()

        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.v_button_layout)
        self.hlayout.addWidget(self.table)
        self.widget = QWidget()
        self.widget.setLayout(self.hlayout)
        self.setCentralWidget(self.widget)
        
        

    def getListFilter(self):
        genders = self.db.query(hotel.Gender).all()
        rooms = self.db.query(hotel.Room).all()
        
        for gender in genders:
            self.gender_list.append(str(gender.gender_name))
        for room in rooms:
            self.room_list.append(str(room.name))
        self.room_list.append("Любой")
        


    def onClickClient(self,text=None):
        
        self.line_find.setPlaceholderText("Поиск по фамилии")
        self.line_find.textChanged.connect(self.searchClient)
        clients = self.getClients(text)
        
        self.table.clear()
        self.table.setRowCount(self.db.query(hotel.Guest).count())
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Пол", "Дата рождения", "Место рождения", "Паспорт", "Телефон"])
        
        self.genderFilter()
        пше
        for i, (c) in enumerate(clients):
            client_id = QTableWidgetItem(str(c.id))
            client_last_name = QTableWidgetItem(str(c.last_name))
            client_first_name = QTableWidgetItem(str(c.first_name))
            client_middle_name = QTableWidgetItem(str(c.middle_name))
            client_gender = QTableWidgetItem(str(c.gender_str.gender_name))
            client_birthday = QTableWidgetItem(str(c.birth_date))
            client_birth_place = QTableWidgetItem(str(c.birth_place))
            client_passport = QTableWidgetItem(str(c.passport_str.passport_series) + " " + str(c.passport_str.passport_number))
            client_phone = QTableWidgetItem(str(c.phone))
            
            self.table.setItem(i,0,client_id)
            self.table.setItem(i,1,client_last_name)
            self.table.setItem(i,2,client_first_name)
            self.table.setItem(i,3,client_middle_name)
            self.table.setItem(i,4,client_gender)
            self.table.setItem(i,5,client_birthday)
            self.table.setItem(i,6,client_birth_place)
            self.table.setItem(i,7,client_passport)
            self.table.setItem(i,8,client_phone)

        self.table.show()
        
    def searchClient(self, text):
        self.table.clear()
        self.onClickClient(text)
        
        
        
    def getClients(self, text=None):
        if text:
            return self.db.query(hotel.Guest).filter(hotel.Guest.last_name.like(f"%{text}%")).all()
        else:
            return self.db.query(hotel.Guest).all()
        
    def genderFilter(self):
        self.combobox.clear()
        self.combobox.addItems(self.gender_list)



        
        
    def onClickRoom(self,text=None):
        self.line_find.setPlaceholderText("Поиск по названию номера")
        self.line_find.textChanged.connect(self.searchRoom)
        
        rooms = self.getRooms(text)
        
        self.roomFilter()
        
        self.table.clear()
        self.table.setRowCount(self.db.query(hotel.Room).count())
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена"])
        for i, (r) in enumerate(rooms):
            room_id = QTableWidgetItem(str(r.id))
            room_name = QTableWidgetItem(str(r.name))
            room_descr = QTableWidgetItem(str(r.description))
            room_price = QTableWidgetItem(str(r.price))
            self.table.setItem(i, 0, room_id)
            self.table.setItem(i, 1, room_name)
            self.table.setItem(i, 2, room_descr)
            self.table.setItem(i, 3, room_price)
            
    def roomFilter(self):
        self.combobox.clear()
        self.combobox.addItems(self.room_list)
            
            
    def searchService(self, text):
        self.table.clear()
        self.onClickService(text)
        
        
        
    def getService(self, text=None):
        if text:
            return self.db.query(hotel.Services).filter(hotel.Services.description.like(f"%{text}%")).all()
        else:
            return self.db.query(hotel.Services).all()
            

    def onClickService(self):
        self.line_find.setPlaceholderText("описание услуги")
        self.line_find.textChanged.connect(self.searchService)
        
        services = self.db.query(hotel.Services).all()
        self.table.clear()
        self.table.setRowCount(self.db.query(hotel.Services).count())
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена"])
        for i, (s) in enumerate(services):
            service_id = QTableWidgetItem(str(s.id))
            service_name = QTableWidgetItem(str(s.name))
            service_descr = QTableWidgetItem(str(s.description))
            service_price = QTableWidgetItem(str(s.price))
            self.table.setItem(i, 0, service_id)
            self.table.setItem(i, 1, service_name)
            self.table.setItem(i, 2, service_descr)
            self.table.setItem(i, 3, service_price)

        self.table.show()
        
    def searchRoom(self, text):
        self.table.clear()
        self.onClickRoom(text)
        
        
        
    def getRooms(self, text=None):
        if text:
            return self.db.query(hotel.Room).filter(hotel.Room.name.like(f"%{text}%")).all()
        else:
            return self.db.query(hotel.Room).all()
        
        
    def onClickBooking(self):
        bookings = self.db.query(hotel.Questionnaire).all()
        self.table.clear()
        self.table.setRowCount(self.db.query(hotel.Services).count())
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Гость", "Срокпроживания", "Комната", "Прибытие", "Отбытие", "Скидка"])
        for i, b in enumerate(bookings):
            booking_id = QTableWidgetItem(str(b.id))
            booking_guest = QTableWidgetItem(str(b.guest_str.last_name + " " + b.guest_str.first_name + " " + b.guest_str.middle_name))
            booking_stay_until = QTableWidgetItem(str(b.stay_until))
            booking_room = QTableWidgetItem(str(b.room_str.name))
            booking_arrival = QTableWidgetItem(str(b.arrival))
            booking_departure = QTableWidgetItem(str(b.departure))
            booking_discount = QTableWidgetItem(str(b.discount))
            self.table.setItem(i,0,booking_id)
            self.table.setItem(i,1,booking_guest)
            self.table.setItem(i,2,booking_stay_until)
            self.table.setItem(i,3,booking_room)
            self.table.setItem(i,4,booking_arrival)
            self.table.setItem(i,5,booking_departure)
            self.table.setItem(i,6,booking_discount)
        self.table.show()

    def closeEvent(self, event):
        self.db.close_all()
        print("Closed")

