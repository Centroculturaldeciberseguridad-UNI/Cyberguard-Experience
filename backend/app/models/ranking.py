from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Puntaje(Base):
    """Un registro por cada reto completado por un usuario."""
    __tablename__ = "puntajes"
    __table_args__ = (
        UniqueConstraint("usuario_id", "reto", name="uq_usuario_reto"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    reto = Column(Integer, nullable=False)          # 1, 2 o 3
    puntos = Column(Integer, nullable=False, default=0)
    completado_at = Column(DateTime, nullable=True)  # se setea al cerrar el reto

    usuario = relationship("Usuario", back_populates="puntajes")

class HallazgoOSINT(Base):
    """Cada hallazgo validado del reto 3 (datos personales)."""
    __tablename__ = "hallazgos_osint"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    clave = Column(String(50), nullable=False)          # ej: "nombre_mascota"
    valor_ingresado = Column(String(200), nullable=False)
    es_correcto = Column(Boolean, nullable=False)
    puntos_obtenidos = Column(Integer, nullable=False, default=0)
    uso_pista_pagada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="hallazgos")

class IntentoPassword(Base):
    """Cada intento de contraseña corporativa del reto 3."""
    __tablename__ = "intentos_password"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    intento_numero = Column(Integer, nullable=False)     # 1, 2 o 3
    password_ingresado = Column(String(100), nullable=False)
    es_correcto = Column(Boolean, nullable=False)
    puntos_obtenidos = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="intentos_password")