from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

#config para encriptar la contraseña 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# clave secreta para firmar los tokens - esto va en el .env
SECRET_KEY = "clave_secreta_muy_larga_y_dificil_de_adivinar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def encriptar_password(password: str) -> str:
    #recibe la passw en txt y devuelve la version encriptada
    return pwd_context.hash(password)

def verificar_password(password: str, password_encriptado: str) -> bool:
    #compara las passw ingresada con la encriptada que esta guardaba en la base de datos
    return pwd_context.verify(password, password_encriptado)

def crear_token(data: dict) -> str:
    
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)