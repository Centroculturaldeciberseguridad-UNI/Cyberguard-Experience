# ============================================================
# RESPUESTAS CORRETAS DEL RETO OSINT
#     Solo se usa en logic.py para validar respuestas.
# ============================================================

PISTAS = {
    "nombre_mascota": {
        "pregunta": "¿Cuál es el nombre de la mascota de Marco?",
        "etiqueta": "Mascota",
        "valor_esperado": "rocky",
        "puntos": 30,
        "tiene_pista_pagada": False,
    },
    "fecha_nacimiento": {
        "pregunta": "¿Cuál es la fecha de nacimiento de Marco? (formato DD/MM/YY)",
        "etiqueta": "Fecha de Nacimiento",
        "valor_esperado": "15/03/01",
        "puntos": 45,
        "tiene_pista_pagada": False,
    },
    "ciudad_residencia": {
        "pregunta": "¿En qué ciudad vive Marco?",
        "etiqueta": "Ciudad",
        "valor_esperado": "lima",
        "puntos": 30,
        "tiene_pista_pagada": False,
    },
    "lugar_frecuente": {
        "pregunta": "¿Cuál es el nombre del lugar o cafetería que Marco frecuenta?",
        "etiqueta": "Lugar Frecuente",
        "valor_esperado": "don mamino",
        "puntos": 35,
        "tiene_pista_pagada": False,
    },
    "situacion_sentimental": {
        "pregunta": "¿Marco tiene pareja actualmente? (responde 'sí' o 'no')",
        "etiqueta": "Situación Sentimental",
        "valor_esperado": "no",
        "puntos": 30,
        "tiene_pista_pagada": False,
    },
    "num_familiares": {
        "pregunta": "¿Cuántos hermanos tiene Marco?",
        "etiqueta": "Hermanos",
        "valor_esperado": "2",
        "puntos": 30,
        "tiene_pista_pagada": False,
    },
    "empresa": {
        "pregunta": "¿En qué empresa trabaja Marco?",
        "etiqueta": "Empresa",
        "valor_esperado": "nexova",
        "puntos": 30,
        "tiene_pista_pagada": False,
    },
    "correo_corporativo": {
        "pregunta": "¿Cuál es el correo corporativo de Marco?",
        "etiqueta": "Correo Corporativo",
        "valor_esperado": "marco.arenas@nexova.com",
        "puntos": 70,
        "tiene_pista_pagada": True,
        "costo_pista": 25,
        "texto_pista": (
            "El formato del correo en Nexova es: nombre.apellido@nexova.com"
        ),
    },
}

# Contraseña corporativa: nombre de mascota + fecha de nacimiento (DDMM)
PASSWORD_CORRECTO = "Rocky1503"

# Puntos decrecientes por intento de contraseña
PUNTOS_POR_INTENTO = {1: 200, 2: 120, 3: 60}

# Penalización respuesta incorrecta
FACTOR_PENALIZACION = 4

# Límite de tiempo
LIMITE_TIEMPO_SEGUNDOS = 7*60