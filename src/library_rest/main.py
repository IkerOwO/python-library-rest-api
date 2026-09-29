from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from library_rest.db import get_db
from library_rest.models import Book
from library_rest.users import (
    UserCreate,
    UserManager,
    UserRead,
    UserUpdate,
    auth_backend,
    fastapi_users,
    get_user_manager,
)

# Instanciamos FastAPI
app = FastAPI()

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
def insert_book(title: str, desc: str, price: float, db: Session = Depends(get_db)):
    db_libro = Book(title=title, description=desc, price=price, isAvailable=True)
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
# Registrar usuario
@app.post("/auth/register", response_model=UserRead, status_code=201)
async def register(user_data: UserCreate, user_manager: UserManager = Depends(get_user_manager)):
    return await user_manager.create(user_data, safe=True)

# Login usuario
@app.post("/auth/login", tags=["auth"])
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
    strategy=Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)
    if user is None or not user.is_active:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas!")

    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response

# Rutas automáticas que genera fastapi-users
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users", tags=["users"]
)