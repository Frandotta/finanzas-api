from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoCategoria(enum.Enum):
    ingreso = "ingreso"
    gasto = "gasto"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    transacciones = relationship("Transaccion", back_populates="usuario")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(Enum(TipoCategoria), nullable=False)

    transacciones = relationship("Transaccion", back_populates="categoria")

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha = Column(Date, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="transacciones")
    categoria = relationship("Categoria", back_populates="transacciones")
