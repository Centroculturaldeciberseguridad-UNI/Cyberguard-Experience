import math
import string
import re

# Constantes del Simulador de Fuerza Bruta
PROCESAMIENTO_POR_SEGUNDO = 10_000_000_000  # 10 mil millones de combinaciones / seg
UN_MINUTO = 60
UN_DIA = 86400
UN_ANIO = 31_536_000
CIEN_ANIOS = 100 * UN_ANIO
UN_MILLON_ANIOS = 1_000_000 * UN_ANIO

PUNTOS_MAXIMOS_RETO1 = 200

SECUENCIAS_TECLADO = [
    "qwerty", "asdfgh", "zxcvbn", "123456", "654321", "abcdef", "123456789",
    "ytrewq", "hgfdsa", "nbvcxz", "987654321",
    "qaz", "wsx", "edc", "rfv", "tgb", "yhn", "ujm", "ikm", "olp",
    "zaq", "xsw", "cde", "vfr", "bgt", "nhy", "mju"
]

PALABRAS_DICCIONARIO = [
    "admin", "password", "contrase", "seguridad", "fiee", "uni", "clave", "root", "usuario",
    "cyber", "guard", "login", "access", "sistema", "master", "123456"
]

def desofuscar_leet(texto: str) -> str:
    mapeo = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a', '@': 'a',
        '5': 's', '$': 's', '7': 't', '!': 'i'
    }
    t = texto.lower()
    for leet, normal in mapeo.items():
        t = t.replace(leet, normal)
    return t

def formatear_tiempo(segundos: float) -> str:
    if segundos <= 0:
        return "0 segundos"
    if segundos < 1:
        return f"{segundos:.4f} segundos"
    if segundos < UN_MINUTO:
        return f"{segundos:.1f} segundos"
    if segundos < UN_MINUTO * 60:
        return f"{segundos / UN_MINUTO:.1f} minutos"
    if segundos < UN_DIA:
        return f"{segundos / 3600:.1f} horas"
    if segundos < UN_ANIO:
        return f"{segundos / UN_DIA:.1f} días"
    if segundos < UN_MILLON_ANIOS:
        return f"{segundos / UN_ANIO:.1f} años"
    anios = segundos / UN_ANIO
    return f"{anios:.2e} años"

def evaluar_seguridad_password(password: str, nickname: str = "") -> dict:
    longitud = len(password)
    if longitud == 0:
        return {
            "longitud": 0,
            "tamano_alfabeto": 0,
            "combinaciones": 0,
            "entropia_bits": 0.0,
            "tiempo_segundos": 0.0,
            "tiempo_legible": "0 segundos",
            "nivel": 1,
            "nivel_nombre": "Muy Débil",
            "puntaje": 0,
            "puntos_maximos": PUNTOS_MAXIMOS_RETO1,
            "tiene_vulnerabilidad": True,
            "vulnerabilidades": ["La contraseña está vacía."],
            "sugerencias": ["Ingresa una contraseña para evaluarla."],
            "feedback": "Por favor ingresa una contraseña para evaluar."
        }

    # 1. Alfabeto
    MINUSCULAS = set(string.ascii_lowercase)
    MAYUSCULAS = set(string.ascii_uppercase)
    NUMEROS = set(string.digits)
    SIMBOLOS = set(string.punctuation)

    tiene_minusculas = any(c in MINUSCULAS for c in password)
    tiene_mayusculas = any(c in MAYUSCULAS for c in password)
    tiene_numeros = any(c in NUMEROS for c in password)
    tiene_simbolos = any(c in SIMBOLOS or (not c.isalnum()) for c in password)

    tamano_alfabeto = 0
    if tiene_minusculas: tamano_alfabeto += 26
    if tiene_mayusculas: tamano_alfabeto += 26
    if tiene_numeros: tamano_alfabeto += 10
    if tiene_simbolos: tamano_alfabeto += 32
    if tamano_alfabeto == 0: tamano_alfabeto = 26

    # 2. Combinaciones
    combinaciones = tamano_alfabeto ** longitud

    # 3. Detección de Vulnerabilidades
    vulnerabilidades = []
    texto_desofuscado = desofuscar_leet(password)
    caracteres_unicos = len(set(password))
    proporcion_unicos = caracteres_unicos / longitud
    proporcion_numeros = sum(c.isdigit() for c in password) / longitud

    es_repetitiva = False
    if longitud >= 5 and caracteres_unicos <= 2:
        es_repetitiva = True
    elif longitud >= 10 and caracteres_unicos <= 3:
        es_repetitiva = True
    elif longitud >= 8 and proporcion_unicos < 0.25:
        es_repetitiva = True
    elif longitud >= 8 and proporcion_numeros > 0.85:
        es_repetitiva = True

    if es_repetitiva:
        vulnerabilidades.append("Caracteres muy repetitivos o poca variedad.")

    es_periodica = False
    if longitud >= 6:
        es_periodica = (password in (password + password)[1:-1])
        if not es_periodica:
            limpia = "".join(c for c in password.lower() if c.isalnum())
            if len(limpia) >= 6:
                es_periodica = (limpia in (limpia + limpia)[1:-1])

    if es_periodica:
        vulnerabilidades.append("Patrón periódico o repetido en bloque.")

    contiene_username = False
    if nickname and len(nickname) >= 3:
        user_lower = nickname.lower()
        user_desofuscado = desofuscar_leet(user_lower)
        user_reverse = user_desofuscado[::-1]
        if (user_desofuscado in password.lower() or 
            user_desofuscado in texto_desofuscado or 
            user_reverse in password.lower() or 
            user_reverse in texto_desofuscado):
            contiene_username = True
        else:
            partes = re.findall(r'[a-zñáéíóúü]+|\d+', user_desofuscado)
            for p in partes:
                if len(p) >= 3:
                    p_rev = p[::-1]
                    if (p in password.lower() or p in texto_desofuscado or 
                        p_rev in password.lower() or p_rev in texto_desofuscado):
                        contiene_username = True
                        break

    if contiene_username:
        vulnerabilidades.append(f"Contiene tu nickname ('{nickname}') o variantes.")

    contiene_secuencia = any(seq in password.lower() for seq in SECUENCIAS_TECLADO)
    if contiene_secuencia:
        vulnerabilidades.append("Contiene secuencias comunes de teclado o números correlativos.")

    contiene_palabra_comun = any(palabra in texto_desofuscado for palabra in PALABRAS_DICCIONARIO)
    if contiene_palabra_comun:
        vulnerabilidades.append("Contiene palabras comunes o de diccionario.")

    tiene_vulnerabilidad = len(vulnerabilidades) > 0

    # 4. Entropía Shannon
    entropia_bits = longitud * math.log2(tamano_alfabeto)
    if tiene_vulnerabilidad:
        entropia_bits = min(entropia_bits, 14.0)

    # 5. Tiempo de Descifrado
    if tiene_vulnerabilidad:
        tiempo_segundos = 0.5
        tiempo_legible = "Menos de 1 segundo (vulnerable a diccionarios / reglas)"
    else:
        tiempo_segundos = combinaciones / PROCESAMIENTO_POR_SEGUNDO
        tiempo_legible = formatear_tiempo(tiempo_segundos)

    # Tiempos en diferentes hardware para UI
    tiempos_hardware = {
        "cpu_antiguo": formatear_tiempo(combinaciones / 10_000_000) if not tiene_vulnerabilidad else "< 1 seg",
        "gpu_gaming": formatear_tiempo(combinaciones / 1_000_000_000) if not tiene_vulnerabilidad else "< 1 seg",
        "rig_mineria": formatear_tiempo(combinaciones / PROCESAMIENTO_POR_SEGUNDO) if not tiene_vulnerabilidad else "< 1 seg",
        "supercomputadora": formatear_tiempo(combinaciones / 1_000_000_000_000) if not tiene_vulnerabilidad else "< 1 seg"
    }

    # 6. Niveles y Puntajes (Escala 0 a 200 pts)
    if tiempo_segundos <= UN_MINUTO:
        nivel = 1
        nivel_nombre = "Muy Débil"
        puntaje_base = 0
    elif tiempo_segundos <= UN_DIA:
        nivel = 2
        nivel_nombre = "Débil"
        puntaje_base = 50
    elif tiempo_segundos <= CIEN_ANIOS:
        nivel = 3
        nivel_nombre = "Aceptable"
        puntaje_base = 100
    elif tiempo_segundos <= UN_MILLON_ANIOS:
        nivel = 4
        nivel_nombre = "Fuerte"
        puntaje_base = 160
    else:
        nivel = 5
        nivel_nombre = "Extremadamente Fuerte"
        puntaje_base = 200

    if tiene_vulnerabilidad:
        if longitud < 12 or es_repetitiva or es_periodica or contiene_username:
            nivel = 1
            nivel_nombre = "Muy Débil"
            puntaje_base = 0
        else:
            nivel = 2
            nivel_nombre = "Débil"
            puntaje_base = 50

    # 7. Sugerencias
    sugerencias = []
    if longitud < 14:
        sugerencias.append("Aumenta la longitud (mínimo 14 caracteres recomendados)")
    if not tiene_mayusculas:
        sugerencias.append("Agrega letras MAYÚSCULAS")
    if not tiene_numeros:
        sugerencias.append("Incluye números (0-9)")
    if not tiene_simbolos:
        sugerencias.append("Añade símbolos especiales (!, @, #, $, etc.)")

    if tiene_vulnerabilidad:
        feedback = "⚠️ Contraseña vulnerable: " + " ".join(vulnerabilidades)
    elif puntaje_base == 200:
        feedback = "🛡️ ¡Excelente contraseña! Resistente a ataques de fuerza bruta y clústeres de cómputo."
    elif puntaje_base >= 160:
        feedback = "🔒 Muy buena seguridad. Difícil de vulnerar en tiempos razonables."
    elif puntaje_base >= 100:
        feedback = "🔑 Seguridad aceptable, pero susceptible con mayor potencia de cálculo."
    else:
        feedback = "⚠️ Contraseña débil. Se puede quebrar rápidamente con ataques automatizados."

    return {
        "longitud": longitud,
        "tamano_alfabeto": tamano_alfabeto,
        "tiene_minusculas": tiene_minusculas,
        "tiene_mayusculas": tiene_mayusculas,
        "tiene_numeros": tiene_numeros,
        "tiene_simbolos": tiene_simbolos,
        "combinaciones": combinaciones,
        "entropia_bits": round(entropia_bits, 1),
        "tiempo_segundos": tiempo_segundos,
        "tiempo_legible": tiempo_legible,
        "tiempos_hardware": tiempos_hardware,
        "nivel": nivel,
        "nivel_nombre": nivel_nombre,
        "puntaje": puntaje_base,
        "puntos_maximos": PUNTOS_MAXIMOS_RETO1,
        "tiene_vulnerabilidad": tiene_vulnerabilidad,
        "vulnerabilidades": vulnerabilidades,
        "sugerencias": sugerencias,
        "feedback": feedback
    }