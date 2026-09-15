from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.ranking import Puntaje
from app.retos.reto1_AlvaroCa.logic import (
    evaluar_seguridad_password,
    PUNTOS_MAXIMOS_RETO1
)

router = APIRouter(prefix="/reto1", tags=["Reto 1 - Contraseñas y Fuerza Bruta"])

class EvaluarPasswordRequest(BaseModel):
    nickname: str = ""
    password: str = Field(..., max_length=120)

class CompletarReto1Request(BaseModel):
    nickname: str
    puntos: int | None = None

@router.get("/estado")
def estado_reto1():
    return {
        "mensaje": "Reto 1: Seguridad de Contraseñas y Simulador de Fuerza Bruta",
        "puntos_maximos": PUNTOS_MAXIMOS_RETO1
    }

@router.post("/evaluar")
def evaluar_password(data: EvaluarPasswordRequest):
    return evaluar_seguridad_password(password=data.password, nickname=data.nickname)

@router.post("/completar")
def completar_reto1(data: CompletarReto1Request, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nickname == data.nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    puntos_a_guardar = data.puntos if data.puntos is not None else PUNTOS_MAXIMOS_RETO1
    puntos_a_guardar = max(0, min(PUNTOS_MAXIMOS_RETO1, puntos_a_guardar))

    existente = db.query(Puntaje).filter(
        Puntaje.usuario_id == usuario.id, Puntaje.reto == 1
    ).first()

    if existente:
        # Actualizamos si el nuevo puntaje es mayor
        if puntos_a_guardar > existente.puntos:
            existente.puntos = puntos_a_guardar
            existente.completado_at = datetime.now(timezone.utc)
            db.commit()
            return {"reto": 1, "puntos": existente.puntos, "mensaje": "Puntaje actualizado con tu mejor marca."}
        return {"reto": 1, "puntos": existente.puntos, "mensaje": "Ya completado anteriormente."}

    puntaje = Puntaje(
        usuario_id=usuario.id,
        reto=1,
        puntos=puntos_a_guardar,
        completado_at=datetime.now(timezone.utc),
    )
    db.add(puntaje)
    db.commit()
    return {"reto": 1, "puntos": puntos_a_guardar, "mensaje": "Reto 1 completado exitosamente."}