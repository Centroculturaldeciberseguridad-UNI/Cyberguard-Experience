import json
import random
import os
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "scenarios.json"

PUNTOS_MAXIMOS_RETO2 = 300
HINT_PENALTY_RATIO = 0.30
WRONG_ANSWER_PENALTY_RATIO = 0.50

DIFFICULTY_POINTS = {
    "easy": 40,
    "medium": 50,
    "hard": 60,
}

_scenarios_cache = None

def cargar_escenarios() -> list[dict]:
    global _scenarios_cache
    if _scenarios_cache is None:
        if not DATA_FILE.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {DATA_FILE}")
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            _scenarios_cache = json.load(f)
    return _scenarios_cache

# Sesiones activas en memoria por nickname
_sesiones_usuario: dict[str, dict] = {}

def crear_sesion_reto2(nickname: str) -> dict:
    escenarios = cargar_escenarios()
    
    por_dificultad = {"easy": [], "medium": [], "hard": []}
    for e in escenarios:
        diff = e.get("difficulty", "easy")
        if diff in por_dificultad:
            por_dificultad[diff].append(e)

    # 2 casos fáciles, 2 medios, 2 difíciles (Total: 6 casos, máx 300 pts)
    seleccionados = []
    for diff in ["easy", "medium", "hard"]:
        pool = por_dificultad[diff]
        k = min(2, len(pool))
        seleccionados.extend(random.sample(pool, k=k))

    random.shuffle(seleccionados)

    sesion = {
        "nickname": nickname,
        "escenarios": seleccionados,
        "current_index": 0,
        "hint_used_current": False,
        "respuestas": [],
        "puntaje_acumulado": 0,
        "completado": False,
    }
    _sesiones_usuario[nickname] = sesion
    return sesion

def obtener_sesion_reto2(nickname: str) -> dict:
    if nickname not in _sesiones_usuario:
        return crear_sesion_reto2(nickname)
    return _sesiones_usuario[nickname]

def obtener_caso_actual(nickname: str) -> dict:
    sesion = obtener_sesion_reto2(nickname)
    if sesion["completado"] or sesion["current_index"] >= len(sesion["escenarios"]):
        return {"completado": True, "puntaje_total": max(0, sesion["puntaje_acumulado"])}

    escenario = sesion["escenarios"][sesion["current_index"]]
    diff = escenario.get("difficulty", "easy")
    puntos_base = escenario.get("base_points") or DIFFICULTY_POINTS.get(diff, 50)

    return {
        "caso_numero": sesion["current_index"] + 1,
        "total_casos": len(sesion["escenarios"]),
        "difficulty": diff,
        "sender_name": escenario["sender_name"],
        "sender_email": escenario["sender_email"],
        "subject": escenario["subject"],
        "body": escenario["body"],
        "display_url": escenario.get("display_url"),
        "base_points": puntos_base,
        "hint_used": sesion["hint_used_current"],
        "puntaje_acumulado": max(0, sesion["puntaje_acumulado"]),
        "completado": False,
    }

def usar_pista(nickname: str) -> dict:
    sesion = obtener_sesion_reto2(nickname)
    if sesion["completado"] or sesion["current_index"] >= len(sesion["escenarios"]):
        return {"error": "El reto ya está completado"}

    escenario = sesion["escenarios"][sesion["current_index"]]
    sesion["hint_used_current"] = True
    return {
        "hint": escenario.get("hint", "Presta atención al remitente y al dominio."),
        "penalizacion": "30% de los puntos de este caso"
    }

def responder_caso(nickname: str, user_answer: bool) -> dict:
    sesion = obtener_sesion_reto2(nickname)
    if sesion["completado"] or sesion["current_index"] >= len(sesion["escenarios"]):
        return {
            "completado": True,
            "puntaje_total": max(0, min(PUNTOS_MAXIMOS_RETO2, sesion["puntaje_acumulado"]))
        }

    escenario = sesion["escenarios"][sesion["current_index"]]
    diff = escenario.get("difficulty", "easy")
    puntos_base = escenario.get("base_points") or DIFFICULTY_POINTS.get(diff, 50)
    is_phishing = escenario["is_phishing"]

    es_correcta = (user_answer == is_phishing)
    puntos_ganados = 0

    if es_correcta:
        puntos_ganados = puntos_base
        if sesion["hint_used_current"]:
            puntos_ganados -= round(puntos_base * HINT_PENALTY_RATIO)
    else:
        puntos_ganados = -round(puntos_base * WRONG_ANSWER_PENALTY_RATIO)

    sesion["puntaje_acumulado"] += puntos_ganados
    sesion["respuestas"].append({
        "caso_id": escenario["id"],
        "user_answer": user_answer,
        "correcta": es_correcta,
        "puntos": puntos_ganados,
        "hint_usado": sesion["hint_used_current"]
    })

    # Avanzar
    sesion["current_index"] += 1
    sesion["hint_used_current"] = False
    
    if sesion["current_index"] >= len(sesion["escenarios"]):
        sesion["completado"] = True

    puntaje_final_actual = max(0, min(PUNTOS_MAXIMOS_RETO2, sesion["puntaje_acumulado"]))

    return {
        "correcta": es_correcta,
        "era_phishing": is_phishing,
        "puntos_ganados": puntos_ganados,
        "puntaje_total_actual": puntaje_final_actual,
        "indicadores": escenario.get("indicators", []),
        "educational_tip": escenario.get("educational_tip", ""),
        "completado": sesion["completado"],
        "siguiente_caso": None if sesion["completado"] else sesion["current_index"] + 1,
        "total_casos": len(sesion["escenarios"])
    }

def obtener_resultado_final_reto2(nickname: str) -> dict:
    sesion = obtener_sesion_reto2(nickname)
    total_casos = len(sesion["escenarios"])
    aciertos = sum(1 for r in sesion["respuestas"] if r["correcta"])
    puntaje = max(0, min(PUNTOS_MAXIMOS_RETO2, sesion["puntaje_acumulado"]))

    return {
        "nickname": nickname,
        "total_casos": total_casos,
        "aciertos": aciertos,
        "errores": total_casos - aciertos,
        "puntaje_obtenido": puntaje,
        "puntos_maximos": PUNTOS_MAXIMOS_RETO2,
        "completado": sesion["completado"]
    }