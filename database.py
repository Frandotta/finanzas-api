from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) #motor de conexión, conecta a PostgreSQL

#Cuando la API necesite hablar con la base de datos, va a abrir una sesión, hacer lo que necesita y cerrarla.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#es la clase base de la que van a heredar todos los modelos.
Base = declarative_base()