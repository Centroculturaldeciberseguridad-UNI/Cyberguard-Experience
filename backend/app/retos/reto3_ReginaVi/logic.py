import re
from app.retos.reto3_ReginaVi.pistas_data import PISTAS, PASSWORD_CORRECTO, PUNTOS_POR_INTENTO, FACTOR_PENALIZACION


def normalizar(valor: str) -> str:
    """
    Normaliza un valor para comparación:
    minúsculas, sin tildes, sin espacios extras.
    """
    valor = valor.strip().lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for original, reemplazo in reemplazos.items():
        valor = valor.replace(original, reemplazo)
    valor = re.sub(r"\s+", " ", valor)
    return valor

def _penalizacion(puntos_posibles: int) -> int:
    """Devuelve la penalizacion por respuesta incorrecta"""
    return -(puntos_posibles//FACTOR_PENALIZACION)

def validar_hallazgo(clave: str, valor_ingresado: str) -> dict:
    """Valida un hallazgo enviado por el participante (sin pista pagada)."""
    if clave not in PISTAS:
        return {"error": "Pista no encontrada."}

    pista = PISTAS[clave]
    es_correcto = normalizar(valor_ingresado) == normalizar(pista["valor_esperado"])
    puntos = pista["puntos"] if es_correcto else _penalizacion(pista["puntos"])

    return {
        "clave": clave,
        "es_correcto": es_correcto,
        "puntos_obtenidos": puntos,
    }


def validar_hallazgo_con_pista_pagada(clave: str, valor_ingresado: str) -> dict:
    """Valida un hallazgo cuando el participante usó la pista pagada."""
    if clave not in PISTAS:
        return {"error": "Pista no encontrada."}

    pista = PISTAS[clave]

    if not pista.get("tiene_pista_pagada", False):
        return {"error": "Esta pista no tiene opción de pista pagada."}

    es_correcto = normalizar(valor_ingresado) == normalizar(pista["valor_esperado"])
    if es_correcto:
        puntos = max(pista["puntos"] - pista["costo_pista"], 0)
    else:
        puntos = _penalizacion(pista["puntos"])

    return {
        "clave": clave,
        "es_correcto": es_correcto,
        "puntos_obtenidos": puntos,
    }


def validar_password(password_ingresado: str, intento_numero: int) -> dict:
    """Valida si la contraseña corporativa ingresada es correcta."""
    if intento_numero < 1 or intento_numero > 3:
        return {"error": "Número de intento inválido."}

    es_correcto = password_ingresado.strip() == PASSWORD_CORRECTO
    puntos = PUNTOS_POR_INTENTO[intento_numero] if es_correcto else 0

    return {
        "intento_numero": intento_numero,
        "es_correcto": es_correcto,
        "puntos_obtenidos": puntos,
        "intentos_restantes": 3 - intento_numero,
        "reto_completado": es_correcto or intento_numero >= 3,
    }


def obtener_info_pista_pagada(clave: str) -> dict | None:
    """Retorna información de la pista pagada si existe para esta clave."""
    if clave not in PISTAS:
        return None
    pista = PISTAS[clave]
    if not pista.get("tiene_pista_pagada", False):
        return None
    return {
        "clave": clave,
        "texto_pista": pista["texto_pista"],
        "costo_pista": pista["costo_pista"],
    }


def obtener_preguntas_pistas() -> list[dict]:
    """Retorna las preguntas de cada pista SIN revelar las respuestas."""
    return [
        {
            "clave": clave,
            "pregunta": datos["pregunta"],
            "etiqueta": datos["etiqueta"],
            "puntos": datos["puntos"],
            "tiene_pista_pagada": datos.get("tiene_pista_pagada", False),
        }
        for clave, datos in PISTAS.items()
    ]
