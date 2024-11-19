from sqlalchemy import ( # Импортируем классы из библиотеки SQLAlchemy для работы с базами данных
Column, # Класс для определения столбцов таблицы
Integer, # Тип данных для целых чисел
String,
Float, # Тип данных для строк
Date, # Тип данных для дат
)

from sqlalchemy.ext.declarative import declarative_base # Импортируем классдля создания моделей данных
from sqlalchemy import create_engine # Импортируем класс для созданияподключения к базе данных
from sqlalchemy.orm import sessionmaker # Импортируем класс для создания сессий
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base() # Создаем объект declarative_base(), который будет использоваться для определения моделей данных

class Issued_by(Base):
    __tablename__ = "issued_by"
    id = Column(Integer, primary_key = True)
    issued_by = Column(String)

class Passport(Base):
    __tablename__ = "passport"
    id = Column(Integer, primary_key = True)
    passport_series = Column(Integer)
    passport_number = Column(Integer)
    issued_by = Column(Integer, ForeignKey(Issued_by.id))
    issued_str = relationship("Issued_by")
    
class Gender(Base):
    __tablename__ = "gender"
    id = Column(Integer, primary_key = True)
    gender_name = Column(String)
    
class Guest(Base): # Определяем класс User, наследующий от Base, который представляет собой модель данных для таблицы users
    __tablename__ = "guest" # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key=True) # Определяем столбец user_id как первичный ключ типа Integer

    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    passport = Column(Integer, ForeignKey(Passport.id))
    phone = Column(String)
    gender_id = Column(Integer, ForeignKey(Gender.id))
    passport_str = relationship("Passport")
    questionnaire = relationship("Questionnaire", back_populates="guest_str", cascade="all,delete")
    gender_str = relationship("Gender")

class Room(Base):
    __tablename__ = "room" # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    questionnaire = relationship("Questionnaire", back_populates="room_str")

class Questionnaire(Base):
    __tablename__ = "questionnaire" # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key=True) # Определяем столбец user_id какпервичный ключ типа Integer
    guest = Column(Integer, ForeignKey(Guest.id))
    stay_until = Column(Date)
    room = Column(Integer, ForeignKey(Room.id))
    arrival = Column(Date)
    departure = Column(Date)
    discount = Column(Integer)
    guest_str = relationship("Guest", back_populates="questionnaire")
    room_str = relationship("Room", back_populates="questionnaire")

class Services(Base):
    __tablename__ = "services" # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

class Services_in_questionnaire(Base):
    __tablename__ = "services_in_questionnaire" # Указываем имя таблицы в базе данных
    id = Column(Integer, primary_key = True)
    questionnaire_id = Column(Integer, ForeignKey(Questionnaire.id))
    service_id = Column(Integer, ForeignKey(Services.id))

def create_connection(login, base):
    # postgresql://admin:root@localhost:5432/hotel
    engine = create_engine(f"postgresql://admin:root@localhost:5432/hotel",
    echo = True) # Создаем объект Engine для подключения к базе данных
    Base.metadata.create_all(engine) # Создаем таблицу users в базе данных, если она еще не существует
    Session = sessionmaker(bind=engine) # Создаем фабрику сессий
    session = Session(bind = engine) # Создаем сессию для работы с базой данных
    return session