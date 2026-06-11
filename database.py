from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:171928Fran1@localhost/finanzas"

engine = create_engine(DATABASE_URL) #motor de conexión, conecta a PostgreSQL

#Cuando la API necesite hablar con la base de datos, va a abrir una sesión, hacer lo que necesita y cerrarla.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#es la clase base de la que van a heredar todos los modelos.
Base = declarative_base()