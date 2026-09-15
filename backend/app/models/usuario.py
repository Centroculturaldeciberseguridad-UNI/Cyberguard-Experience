from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(30), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reto3_iniciado_en = Column(DateTime, nullable=True)

    # Relaciones
    puntajes = relationship("Puntaje", back_populates="usuario", cascade="all, delete-orphan")
    hallazgos = relationship("HallazgoOSINT", back_populates="usuario", cascade="all, delete-orphan")
    intentos_password = relationship("IntentoPassword", back_populates="usuario", cascade="all, delete-orphan")
