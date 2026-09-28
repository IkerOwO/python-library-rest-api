from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

# Cargamos del .env las variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
password = os.getenv("MYSQL_PASS")
user = os.getenv("MYSQL_USER")
db = os.getenv("DATABASE_NAME")

# Creamos la conexion
engine = create_engine(f'mysql+mysqlconnector://{user}/{password}@localhost/{db}')
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Creamos la funcion que usaremos mas tarde para las queries
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()