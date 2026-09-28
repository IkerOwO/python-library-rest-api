from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from library_rest.db import *
from library_rest.models import *
import bcrypt
# from pydantic import BaseModel

app = FastAPI()

# Generamos el Salt
salt = bcrypt.gensalt()

# Endpoints Libro
# Sacar libro mediante titulo
@app.get("/book/{title}")
def get_by_title(book: Book, db: Session = Depends(get_db)):
    pass



# Endpoints Usuarios
# Registrar usuario
@app.post("/auth/create")
def register_user(user: User, db: Session = Depends(get_db)):
    pass



"""
# Hashing
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

# Verificación
if bcrypt.checkpw(password, hashed):
    print("La contraseña coincide")
"""