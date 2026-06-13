from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Usuario
from auth import encriptar_password, verificar_password, crear_token, obtener_usuario_actual

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

class CategoriaCrear(BaseModel):
    nombre: str
    tipo: str

@router.post("/categorias")
def crear_categorias(categoria: CategoriaCrear, db: Session = Depends(get_db),email: str = Depends(obtener_usuario_actual)):
    #solo los logueados crearan categorias y el email viene del token JTW
    from models import Categoria, TipoCategoria

    #verificacion de que el tipo sea valido
    if categoria.tipo not in ["ingreso", "gasto"]:
        raise HTTPException(status_code=401, detail="el tipo debe ser de ingreso o gasto")
    
    #creamos la categoria
    nueva_categoria = Categoria(
        nombre = categoria.nombre,
        tipo = TipoCategoria(categoria.tipo)
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return {"id": nueva_categoria.id, "nombre": nueva_categoria.nombre, "tipo": nueva_categoria.tipo.value}

@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db), email: str = Depends(obtener_usuario_actual)):
    #traemos de la base de datos las categorias
    from models import Categoria
    categorias = db.query(Categoria).all()
    return [{"id": c.id, "nombre": c.nombre, "tipo": c.tipo.value} for c in categorias]

#el esquema de la transaccion
class TransaccionCrear(BaseModel):
    monto: float
    descripcion: str = None
    fecha: str
    categoria_id: int

@router.post("/transacciones")
def crear_transaccion(transaccion: TransaccionCrear, db = Depends(get_db), email: str = Depends(obtener_usuario_actual)):
    from models import Transaccion, Usuario
    from datetime import date

    #buscamos el usuario por email para que nos de su ID
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    #conversion de fecha a objeto
    fecha_convertida = date.fromisoformat(transaccion.fecha)

    #creacion de la transaccion
    nueva_transaccion = Transaccion(
        monto=transaccion.monto,
        descripcion=transaccion.descripcion,
        fecha=fecha_convertida,
        usuario_id=usuario.id,
        categoria_id=transaccion.categoria_id
    )
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)

    return {
        "id": nueva_transaccion.id,
        "monto": nueva_transaccion.monto,
        "descripcion": nueva_transaccion.descripcion,
        "fecha": str(nueva_transaccion.fecha),
        "categoria_id": nueva_transaccion.categoria_id
    }
