import library_rest.db as db
from sqlalchemy import Column, String, Integer, Float, Boolean

# Modelos / Tablas
# Modelo de libro
class Book(db.Base):
    __tablename__ = 'book'

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

    def __repr__(self):
        return f'Book({self.title}, {self.description}, {self.price})'

    def __str__(self):
        return self.title

# Modelo de usuario
class User(db.Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(40), nullable=False)
    password = Column(String(100), nullable=False)
    isActive = Column(Boolean, default=True, nullable=False)

    def __init__(self, username, email, password, isActive):
        self.username = username
        self.email = email
        self.password = password
        self.isActive = isActive

    
