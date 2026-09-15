from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.ranking import Puntaje
from app.retos.reto2_MartinBe.logic import (
    crear_sesion_reto2,
    obtener_caso_actual,
    usar_pista,
    responder_caso,
    obtener_resultado_final_reto2,
    PUNTOS_MAXIMOS_RETO2
)

router = APIRouter(prefix="/reto2", tags=["Reto 2 - Detección de Phishing"])

class SessionRequest(BaseModel):
    nickname: str

class HintRequest(BaseModel):
    nickname: str

class AnswerRequest(BaseModel):
    nickname: str
    user_answer: bool  # True si cree que es phishing, False si cree que es legítimo

class CompletarRequest(BaseModel):
    nickname: str
    puntos: int | None = None

@router.get("/estado")
def estado_reto2():
    return {
        "mensaje": "Reto 2: Phishing Detective",
        "puntos_maximos": PUNTOS_MAXIMOS_RETO2
    }

@router.post("/session")
def iniciar_sesion(data: SessionRequest):
    sesion = crear_sesion_reto2(data.nickname)
    return {
        "status": "created",
        "nickname": data.nickname,
        "total_casos": len(sesion["escenarios"]),
        "puntos_maximos": PUNTOS_MAXIMOS_RETO2
    }

@router.get("/current/{nickname}")
def ver_caso_actual(nickname: str):
    return obtener_caso_actual(nickname)

@router.post("/hint")
def solicitar_pista(data: HintRequest):
    return usar_pista(data.nickname)

@router.post("/answer")
def enviar_respuesta(data: AnswerRequest, db: Session = Depends(get_db)):
    feedback = responder_caso(nickname=data.nickname, user_answer=data.user_answer)
    
    # Si completó todos los casos, guardar automáticamente en la base de datos
    if feedback.get("completado"):
        puntos_finales = feedback.get("puntaje_total_actual", 0)
        usuario = db.query(Usuario).filter(Usuario.nickname == data.nickname).first()
        if usuario:
            existente = db.query(Puntaje).filter(
                Puntaje.usuario_id == usuario.id, Puntaje.reto == 2
            ).first()
            if existente:
                if puntos_finales > existente.puntos:
                    existente.puntos = puntos_finales
                    existente.completado_at = datetime.now(timezone.utc)
                    db.commit()
            else:
                puntaje = Puntaje(
                    usuario_id=usuario.id,
                    reto=2,
                    puntos=puntos_finales,
                    completado_at=datetime.now(timezone.utc),
                )
                db.add(puntaje)
                db.commit()

    return feedback

@router.get("/result/{nickname}")
def resultado_reto2(nickname: str):
    return obtener_resultado_final_reto2(nickname)

@router.post("/completar")
def completar_reto2(data: CompletarRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nickname == data.nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    puntos = data.puntos if data.puntos is not None else PUNTOS_MAXIMOS_RETO2
    puntos = max(0, min(PUNTOS_MAXIMOS_RETO2, puntos))

    existente = db.query(Puntaje).filter(
        Puntaje.usuario_id == usuario.id, Puntaje.reto == 2
    ).first()
    if existente:
        if puntos > existente.puntos:
            existente.puntos = puntos
            existente.completado_at = datetime.now(timezone.utc)
            db.commit()
            return {"reto": 2, "puntos": existente.puntos, "mensaje": "Puntaje actualizado."}
        return {"reto": 2, "puntos": existente.puntos, "mensaje": "Ya completado."}

    puntaje = Puntaje(
        usuario_id=usuario.id,
        reto=2,
        puntos=puntos,
        completado_at=datetime.now(timezone.utc),
    )
    db.add(puntaje)
    db.commit()
    return {"reto": 2, "puntos": puntos, "mensaje": "Reto 2 completado."}