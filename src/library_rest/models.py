from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

class Base(DeclarativeBase):
    pass

# Modelos / Tablas
# Modelo de libro
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    isAvailable = Column(Boolean, default=True, nullable=False)

    def __init__(self, title, description, price, isAvailable):
        self.title = title
        self.description = description
        self.price = price
        self.isAvailable = isAvailable

    def __repr__(self):
        return f'Book({self.title}, {self.description}, {self.price}, {self.isAvailable})'

    def __str__(self):
        return self.title

# Modelo de usuario
class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


    
