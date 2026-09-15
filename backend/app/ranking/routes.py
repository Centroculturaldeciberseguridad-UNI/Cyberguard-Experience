from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.ranking.service import calcular_ranking
from app.schemas.ranking_schema import RankingResponse
from app.models.usuario import Usuario
from app.models.ranking import Puntaje

router = APIRouter(prefix="/ranking", tags=["Ranking"])

@router.get("", response_model=RankingResponse)
def obtener_ranking(
    top: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Devuelve el ranking público (nickname + puntos_total)."""
    resultado = calcular_ranking(db, limit=top)
    return RankingResponse(ranking=resultado, total=len(resultado))

@router.get("/posicion/{nickname}")
def obtener_posicion(nickname: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nickname == nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    puntajes = db.query(Puntaje).filter(Puntaje.usuario_id == usuario.id).all()
    desglose = {p.reto: p.puntos for p in puntajes}
    total = sum(desglose.values())

    ranking = calcular_ranking(db, limit=10000)
    posicion = None
    for i, entry in enumerate(ranking):
        if entry["nickname"] == nickname:
            posicion = i+1
            break

    return {
        "posicion": posicion,
        "puntos_total": total,
        "desglose": {
            "reto1": desglose.get(1,0),
            "reto2": desglose.get(2,0),
            "reto3": desglose.get(3,0),
        },
        "en_top10": posicion is not None and posicion <= 10,
        "en_top50": posicion is not None and posicion <= 50,
    }

@router.get("/estado-retos/{nickname}")
def estado_retos(nickname: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nickname == nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    puntajes = db.query(Puntaje).filter(Puntaje.usuario_id == usuario.id).all()
    completados = {p.reto for p in puntajes}

    return {
        "reto1": 1 in completados,
        "reto2": 2 in completados,
        "reto3": 3 in completados,
    }