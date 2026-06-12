from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Usuario
from auth import encriptar_password, verificar_password, crear_token

# podemos interpretarlo como una miniapi donde agrupamos endpoints
router = APIRouter()

#abre y cierra la sesion de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

# datos que el usuario manda para el regsitro
class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

# datos que el usuario manda para el login
class UsuarioLogin(BaseModel):
    email: str
    password: str

@router.post("/registro")
def registro(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    #verificamos que exista el mail
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    
    #encriptar la contraseña antes de guardarla
    password_encriptado = encriptar_password(usuario.password)

    #crear el usuario en la base de datos
    nuevo_usuario = Usuario(
        nombre = usuario.nombre,
        email = usuario.email,
        password = password_encriptado
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"mensaje": "Usuario registrado correctamente", "id": nuevo_usuario.id}

@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    # Buscar el usuario por email
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario:
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    
    # verificamos contraseña
    if not verificar_password(usuario.password, db_usuario.password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    
    # crear y devolver el token JWT
    token = crear_token({"email": db_usuario.email})
    return {"access_token": token, "token_type": "bearer"}