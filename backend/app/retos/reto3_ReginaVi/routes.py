from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.ranking import HallazgoOSINT, IntentoPassword, Puntaje
from app.retos.reto3_ReginaVi.logic import (
    validar_hallazgo,
    validar_hallazgo_con_pista_pagada,
    validar_password,
    obtener_info_pista_pagada,
    obtener_preguntas_pistas,
)
from app.retos.reto3_ReginaVi.perfil_data import PERFIL_MARCO, PERFIL_CARLOS, PERFIL_NEXOVA, PERFIL_CAMILA
from app.retos.reto3_ReginaVi.pistas_data import PISTAS, LIMITE_TIEMPO_SEGUNDOS

router = APIRouter(prefix="/reto3", tags=["Reto 3 — OSINT"])

# ============================================================
# SCHEMAS LOCALES (solo para este módulo)
# ============================================================

class HallazgoRequest(BaseModel):
    nickname: str
    clave: str
    valor: str

class PistaPagadaRequest(BaseModel):
    nickname: str
    clave: str
    valor: str

class PasswordRequest(BaseModel):
    nickname: str
    password: str

class NicknameRequest(BaseModel):
    nickname: str

# ============================================================
# HELPERS
# ============================================================

def _obtener_usuario(db: Session, nickname: str) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.nickname == nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado. Regístrate primero.")
    return usuario

def _segundos_restantes(usuario: Usuario) -> int:
    if not usuario.reto3_iniciado_en:
        return LIMITE_TIEMPO_SEGUNDOS
    transcurrido = (datetime.utcnow()-usuario.reto3_iniciado_en).total_seconds()
    return max(int(LIMITE_TIEMPO_SEGUNDOS - transcurrido), 0)

def _guardar_puntaje_final(db: Session, usuario: Usuario) -> Puntaje:
    """Suma los puntos actuales del reto 3 y crea el puntaje"""
    hallazgos = db.query(HallazgoOSINT).filter(HallazgoOSINT.usuario_id == usuario.id).all()
    intentos = db.query(IntentoPassword).filter(IntentoPassword.usuario_id == usuario.id).all()

    puntos_hallazgos = sum(h.puntos_obtenidos for h in hallazgos)
    puntos_password = sum(i.puntos_obtenidos for i in intentos)
    puntos_total = max(puntos_hallazgos+puntos_password, 0)

    puntaje = Puntaje(
        usuario_id = usuario.id,
        reto = 3,
        puntos = puntos_total,
        completado_at = datetime.now(timezone.utc),
    )
    db.add(puntaje)
    db.commit()
    db.refresh(puntaje)
    return puntaje

def _cerrar_reto(db: Session, usuario: Usuario) -> Puntaje | None:
    """Si hay puntaje para el reto 3 no hace nada. En caso no
    haya puntaje y el tiempo se agota, se cierra el reto con
    el puntaje obtenido."""
    existente = (
        db.query(Puntaje)
        .filter(Puntaje.usuario_id == usuario.id, Puntaje.reto == 3)
        .first()
    )
    if existente:
        return existente

    if _segundos_restantes(usuario)>0:
        return None

    return _guardar_puntaje_final(db, usuario)

def _bloquear_tiempo_agotado(db: Session, usuario: Usuario):
    cerrado = _cerrar_reto(db, usuario)
    if cerrado:
        raise HTTPException(status_code=403, detail="Se acabó el tiempo para este reto.")

# ============================================================
# ENDPOINTS PÚBLICOS — Contenido del sandbox
# ============================================================

@router.get("/perfil/marco")
def get_perfil_marco():
    return PERFIL_MARCO

@router.get("/perfil/carlos")
def get_perfil_carlos():
    return PERFIL_CARLOS

@router.get("/perfil/nexova")
def get_perfil_nexova():
    return PERFIL_NEXOVA

@router.get("/perfil/camila")
def get_perfil_camila():
    return PERFIL_CAMILA

@router.get("/pistas")
def get_pistas():
    """Preguntas de las pistas (sin revelar respuestas correctas)."""
    return obtener_preguntas_pistas()

# ============================================================
# ENDPOINTS Control de tiempo
# ============================================================

@router.post("/iniciar")
def iniciar_reto3(data: NicknameRequest, db: Session = Depends(get_db)):
    """Marca el inicio del cronometro"""
    usuario = _obtener_usuario(db, data.nickname)
    if not usuario.reto3_iniciado_en:
        usuario.reto3_iniciado_en = datetime.utcnow()
        db.commit()
        db.refresh(usuario)

    return {
        "segundos_restantes": _segundos_restantes(usuario),
        "limite_segundos": LIMITE_TIEMPO_SEGUNDOS,
    }

@router.post("/finalizar")
def finalizar_reto3(data: NicknameRequest, db: Session = Depends(get_db)):
    """Terminar voluntariamente el reto con el puntaje acumulado hasta ese momento"""
    usuario = _obtener_usuario(db, data.nickname)
    puntaje = _cerrar_reto(db, usuario) or _guardar_puntaje_final(db, usuario)

    return {
        "puntos_tota_reto3": puntaje.puntos,
        "reto_completado": True,
    }

# ============================================================
# ENDPOINTS DE VALIDACIÓN — Hallazgos (Bloque A)
# ============================================================

@router.post("/hallazgo")
def enviar_hallazgo(data: HallazgoRequest, db: Session = Depends(get_db)):
    """Envía un hallazgo del expediente para ser validado (sin pista pagada)."""
    usuario = _obtener_usuario(db, data.nickname)
    _bloquear_tiempo_agotado(db, usuario)

    # ¿Ya respondió esta pista?
    existente = (
        db.query(HallazgoOSINT)
        .filter(HallazgoOSINT.usuario_id == usuario.id, HallazgoOSINT.clave == data.clave)
        .first()
    )
    if existente:
        raise HTTPException(status_code=409, detail="Ya respondiste esta pista.")

    resultado = validar_hallazgo(data.clave, data.valor)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])

    hallazgo = HallazgoOSINT(
        usuario_id=usuario.id,
        clave=data.clave,
        valor_ingresado=data.valor.strip(),
        es_correcto=resultado["es_correcto"],
        puntos_obtenidos=resultado["puntos_obtenidos"],
        uso_pista_pagada=False,
    )
    db.add(hallazgo)
    db.commit()
    db.refresh(hallazgo)

    return {
        "clave": data.clave,
        "es_correcto": resultado["es_correcto"],
        "puntos_obtenidos": resultado["puntos_obtenidos"],
    }

# ============================================================
# ENDPOINTS — Pista pagada (correo corporativo)
# ============================================================

@router.get("/pista-pagada/{clave}")
def get_info_pista_pagada(clave: str):
    """Devuelve la info de la pista pagada si existe (texto y costo)."""
    info = obtener_info_pista_pagada(clave)
    if not info:
        raise HTTPException(status_code=404, detail="No hay pista pagada disponible para esta clave.")
    return info

@router.post("/pista-pagada")
def usar_pista_pagada(data: PistaPagadaRequest, db: Session = Depends(get_db)):
    """Envía hallazgo usando la pista pagada (se aplica costo si acierta)."""
    usuario = _obtener_usuario(db, data.nickname)
    _bloquear_tiempo_agotado(db, usuario)

    existente = (
        db.query(HallazgoOSINT)
        .filter(HallazgoOSINT.usuario_id == usuario.id, HallazgoOSINT.clave == data.clave)
        .first()
    )
    if existente:
        raise HTTPException(status_code=409, detail="Ya respondiste esta pista.")

    resultado = validar_hallazgo_con_pista_pagada(data.clave, data.valor)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])

    hallazgo = HallazgoOSINT(
        usuario_id=usuario.id,
        clave=data.clave,
        valor_ingresado=data.valor.strip(),
        es_correcto=resultado["es_correcto"],
        puntos_obtenidos=resultado["puntos_obtenidos"],
        uso_pista_pagada=True,
    )
    db.add(hallazgo)
    db.commit()
    db.refresh(hallazgo)

    return {
        "clave": data.clave,
        "es_correcto": resultado["es_correcto"],
        "puntos_obtenidos": resultado["puntos_obtenidos"],
        "pista_texto": PISTAS[data.clave]["texto_pista"],
    }

# ============================================================
# ENDPOINTS — Contraseña corporativa (Bloque B)
# ============================================================

@router.post("/password")
def intentar_password(data: PasswordRequest, db: Session = Depends(get_db)):
    """Intenta adivinar la contraseña corporativa (máx. 3 intentos)."""
    usuario = _obtener_usuario(db, data.nickname)
    _bloquear_tiempo_agotado(db, usuario)

    # Verificar intentos previos
    intentos_previos = (
        db.query(IntentoPassword)
        .filter(IntentoPassword.usuario_id == usuario.id)
        .order_by(IntentoPassword.intento_numero)
        .all()
    )

    if len(intentos_previos) >= 3:
        raise HTTPException(status_code=403, detail="Ya agotaste tus 3 intentos.")

    if any(i.es_correcto for i in intentos_previos):
        raise HTTPException(status_code=403, detail="Ya acertaste la contraseña anteriormente.")

    intento_numero = len(intentos_previos) + 1
    resultado = validar_password(data.password, intento_numero)

    # Guardar intento
    intento = IntentoPassword(
        usuario_id=usuario.id,
        intento_numero=intento_numero,
        password_ingresado=data.password.strip(),
        es_correcto=resultado["es_correcto"],
        puntos_obtenidos=resultado["puntos_obtenidos"],
    )
    db.add(intento)
    db.commit()

    if resultado["reto_completado"]:
        _guardar_puntaje_final(db, usuario)

    return {
        "intento_numero": intento_numero,
        "es_correcto": resultado["es_correcto"],
        "puntos_obtenidos": resultado["puntos_obtenidos"],
        "intentos_restantes": resultado["intentos_restantes"],
        "reto_completado": resultado["reto_completado"],
    }

# ============================================================
# ENDPOINT — Progreso del participante
# ============================================================

@router.get("/progreso/{nickname}")
def obtener_progreso(nickname: str, db: Session = Depends(get_db)):
    """Retorna el progreso actual del participante en el reto 3."""
    usuario = _obtener_usuario(db, nickname)
    _cerrar_reto(db, usuario) # cierra el reto si el tiempo se acaba

    hallazgos = (
        db.query(HallazgoOSINT)
        .filter(HallazgoOSINT.usuario_id == usuario.id)
        .all()
    )
    intentos = (
        db.query(IntentoPassword)
        .filter(IntentoPassword.usuario_id == usuario.id)
        .order_by(IntentoPassword.intento_numero)
        .all()
    )
    puntaje = (
        db.query(Puntaje)
        .filter(Puntaje.usuario_id == usuario.id, Puntaje.reto == 3)
        .first()
    )

    puntos_hallazgos = sum(h.puntos_obtenidos for h in hallazgos)
    puntos_password = sum(i.puntos_obtenidos for i in intentos)

    # El reto se considera completado si hay Puntaje (se creó al cerrar)
    reto_completado = puntaje is not None

    return {
        "hallazgos": [
            {
                "clave": h.clave,
                "valor_ingresado": h.valor_ingresado,
                "es_correcto": h.es_correcto,
                "puntos_obtenidos": h.puntos_obtenidos,
                "uso_pista_pagada": h.uso_pista_pagada,
            }
            for h in hallazgos
        ],
        "intentos_password": [
            {
                "intento_numero": i.intento_numero,
                "es_correcto": i.es_correcto,
                "puntos_obtenidos": i.puntos_obtenidos,
            }
            for i in intentos
        ],
        "puntos_hallazgos": puntos_hallazgos,
        "puntos_password": puntos_password,
        "puntos_total_reto3": puntaje.puntos if puntaje else max(puntos_hallazgos + puntos_password, 0),
        "reto_completado": reto_completado,
        "segundos_restantes": _segundos_restantes(usuario),
        "tiempo_agotado": _segundos_restantes(usuario) <= 0,
    }
