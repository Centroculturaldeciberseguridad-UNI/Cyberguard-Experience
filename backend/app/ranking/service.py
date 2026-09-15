from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.usuario import Usuario
from app.models.ranking import Puntaje

def calcular_ranking(db: Session, limit: int = 10) -> list[dict]:
    """
    Calcula el ranking público sumando puntos de todos los retos completados.
    Desempate: si dos usuarios tienen el mismo puntaje, gana quien completó
    su último reto primero (timestamp más antiguo).
    """
    resultados = (
        db.query(
            Usuario.nickname,
            func.coalesce(func.sum(Puntaje.puntos), 0).label("puntos_total"),
            func.max(Puntaje.completado_at).label("ultimo_reto"),
        )
        .outerjoin(Puntaje, Puntaje.usuario_id == Usuario.id)
        .group_by(Usuario.id)
        .having(func.coalesce(func.sum(Puntaje.puntos), 0) > 0)
        .order_by(
            func.coalesce(func.sum(Puntaje.puntos), 0).desc(),
            func.max(Puntaje.completado_at).asc(),   # desempate
        )
        .limit(limit)
        .all()
    )

    return [
        {"nickname": r.nickname, "puntos_total": r.puntos_total}
        for r in resultados
    ]