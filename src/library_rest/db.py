from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from library_rest.models import User
from dotenv import load_dotenv
import os

# Cargamos del .env las variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
password = os.getenv("MYSQL_PASS")
user = os.getenv("MYSQL_USER")
db = os.getenv("DATABASE_NAME")

# Creamos las conexiones síncrona y asíncrona
sync_url = URL.create(
    "mysql+mysqlconnector",
    username=user,
    password=password,
    host="localhost",
    database=db,
)
async_url = URL.create(
    "mysql+asyncmy",
    username=user,
    password=password,
    host="localhost",
    database=db,
)
engine = create_engine(sync_url)
SessionLocal = sessionmaker(bind=engine)
async_engine = create_async_engine(async_url)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

# Creamos la funcion que usaremos mas tarde para las queries
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_db():
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, User)