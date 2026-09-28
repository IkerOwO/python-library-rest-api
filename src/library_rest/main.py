from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from library_rest.db import *
from library_rest.models import *
import bcrypt

# Instanciamos FastAPI
app = FastAPI()

# Generamos el Salt
salt = bcrypt.gensalt()

# Endpoints Libro
# Sacar libro mediante titulo
@app.get("/book/{title}")
def get_by_title(title: str, db: Session = Depends(get_db)):
    libro = db.query(Book).filter(Book.title == title).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado") 

# Sacar todos los libros
@app.get("/book")
def get_all_books(db: Session = Depends(get_db)):
    query = db.query(Book).all()
    return query

# Insertar nuevo libro
@app.post("/book/create")
def insert_book(title: str, desc: str, price: float, isAvailable: bool, db: Session = Depends(get_db)):
    db_libro = Book(title=title, description=desc, price=price, isAvailable=isAvailable)
    db.add(db_libro)
    db.commit()
    db.refresh()
    return {"detail": "Libro insertado en la base de datos!"}

# Cambiar si esta en stock
@app.put("/book/{book_id}")
def update_availability(book_id: int, isAvailable: bool, db: Session = Depends(get_db)):
    libro = db.query(Book).filter(Book.id == book_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    libro.isAvailable = isAvailable
    db.commit()
    return {"detail": "Stock actualizado con éxito!"}

# Borrar libro
@app.delete("/book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    libro = db.query(Book).filter(Book.id == book_id).first()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    db.refresh()
    return {"detail": "Libro borrado con exito!"}


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