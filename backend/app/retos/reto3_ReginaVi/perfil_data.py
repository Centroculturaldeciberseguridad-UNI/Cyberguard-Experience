# ============================================================
# SANDBOX DE INSTAGRAM
# ============================================================

# ────────────────────────────────────────────────────────────
# PERFIL 1 — Marco Arenas (el objetivo)
# ────────────────────────────────────────────────────────────

PERFIL_MARCO = {
    "id": "marco",
    "username": "marco.arenas01",
    "nombre": "Marco Arenas",
    "foto_url": "/images/marco/marco_perfil.png",
    "bio": "📍 Lima, Perú | ☕ Café & código | 🐕 Padre de Rocky | 💻 Ing. de sistemas en @nexova_oficial",
    "seguidores": 342,
    "publicaciones": 9,

    "posts": [
        {
            "id": "p1",
            "imagen_url": "/images/marco/marco_party.png",
            "caption": "Un año más 🎂 ¡25 añitos! Gracias a todos por las felicitaciones, los quiero mucho ❤️🎉",
            "fecha": "2026-03-15",
            "likes": 112,
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "¡Feliz cumple hermanito! 🎉❤️ Te queremos mucho"},
                {"usuario": "luisfer_22", "texto": "¡Felicidades crack! 🎂🎉"},
                {"usuario": "jessica.m", "texto": "Mi hijo hermoso, que Dios te bendiga siempre ❤️🙏"},
            ],
        },
        {
            "id": "p2",
            "imagen_url": "/images/marco/cafe.jpg",
            "caption": "El San Valentín perfecto: café, libro y paz mental 📚☕ #SolteroFeliz",
            "fecha": "2026-02-14",
            "likes": 88,
            "comentarios": [
                {"usuario": "diego_sistemas", "texto": "¿Otra vez soltero en San Valentín? 😂💔"},
                {"usuario": "marco.arenas01", "texto": "Jajaja ya sabes, mejor solo que mal acompañado 😅"},
                {"usuario": "carlos.arenas_", "texto": "Mi hermano el solterón empedernido 😂💔"},
            ],
        },
        {
            "id": "p3",
            "imagen_url": "/images/marco/rocky02.png",
            "caption": "Rocky esperándome en la puerta como todos los días 🐕❤️ No hay mejor bienvenida después del trabajo",
            "fecha": "2025-05-08",
            "likes": 73,
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "Rocky, el más fiel 🐕"},
                {"usuario": "nexova_oficial", "texto": "¡Mascotas en casa, el mejor equipo de bienvenida! 🐾"},
            ],
        },
        {
            "id": "p4",
            "imagen_url": "/images/marco/01.png",
            "caption": "Equipo Nexova cerrando el Q2 con éxito 💪🚀 Gracias a todos por este gran semestre. ¡Por más logros juntos! #Nexova #Equipo",
            "fecha": "2024-06-30",
            "likes": 104,
            "ubicacion": "Oficinas Nexova, Lima",
            "comentarios": [
                {"usuario": "nexova_oficial", "texto": "¡Gran equipo, grandes resultados! 💪🏢"},
                {"usuario": "luisfer_22", "texto": "¡Felicidades al equipo! 🚀"},
            ],
        },
        {
            "id": "p5",
            "imagen_url": "/images/marco/rocky01.png",
            "caption": "El rey Rocky cumplió 3 años hoy 🐕🎂 ¡El mejor regalo que me ha dado la vida! #PerrosLover #FelizCumpleaños",
            "fecha": "2024-06-13",
            "likes": 58,
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "¡Feliz cumpleaños al mejor sobrino peludo! 🥺❤️"},
                {"usuario": "luisfer_22", "texto": "¡Felicidades Rocky! 🎉🐕"},
            ],
        },
        {
            "id": "p6",
            "imagen_url": "/images/marco/don-mamino02.jpg",
            "caption": "Viernes de café en Don Mamino con buena compañía ☕ El ritual de siempre jaja",
            "fecha": "2023-09-15",
            "likes": 41,
            "ubicacion": "Don Mamino, Lima",
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "¡Otra vez ahí! Ya deberían hacerte socio 😂☕"},
                {"usuario": "luisfer_22", "texto": "¿Me invitan la próxima? 😁"},
            ],
        },
        {
            "id": "p7",
            "imagen_url": "/images/marco/oficina.png",
            "caption": "Primer día en mi nuevo trabajo en Nexova 🚀💻 Emocionado por este nuevo capítulo como ingeniero de sistemas. ¡A darle con todo! #NuevoTrabajo #Nexova",
            "fecha": "2023-01-10",
            "likes": 95,
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "¡Felicidades hermano! Nexova no sabe la suerte que tiene 💪"},
                {"usuario": "diego_sistemas", "texto": "¡Bien ahí bro! ¿Ya te dieron laptop nueva? 😂"},
                {"usuario": "luisfer_22", "texto": "¡Éxito en esta nueva etapa! 🚀"},
            ],
        },
        {
            "id": "p8",
            "imagen_url": "/images/marco/huanchaco-beach.jpg",
            "caption": "Huanchaco, el mejor escape del fin de semana 🏖️ Nada como el mar para recargar energías",
            "fecha": "2022-07-27",
            "likes": 67,
            "ubicacion": "Huanchaco, Trujillo",
            "comentarios": [
                {"usuario": "carlos.arenas_", "texto": "¡La próxima voy con ustedes! 🏖️"},
                {"usuario": "diego_sistemas", "texto": "Huanchaco siempre es buena idea 🌊"},
            ],
        },
        {
            "id": "p9",
            "imagen_url": "/images/marco/don-mamino.jpg",
            "caption": "Oficina del día: Don Mamino ☕💻 El mejor lugar para concentrarse en Lima. Ya casi son de casa jaja",
            "fecha": "2021-11-25",
            "likes": 34,
            "ubicacion": "Don Mamino, Lima",
            "comentarios": [
                {"usuario": "diego_sistemas", "texto": "¡Ese lugar es genial! ¿El wifi ya les funciona bien? 😂"},
            ],
        },
    ],

    "historias_destacadas": [
        {
            "id": "hl1",
            "titulo": "Viaje ✈️",
            "portada_url": "/images/marco/viaje01.jpg",
            "stories": [
                {"id": "s1", "imagen_url": "/images/marco/viaje01.jpg", "texto": "Las vistas del avión", "fecha": "2023-04-15"},
                {"id": "s2", "imagen_url": "/images/marco/viaje02.jpg", "texto": "Bello paisaje", "fecha": "2023-04-20"},
                {"id": "s3", "imagen_url": "/images/marco/viaje03.jpg", "texto": "Que cielo más bonito", "fecha": "2023-04-21"},
            ],
        },
        {
            "id": "hl2",
            "titulo": "Trabajo 💼",
            "portada_url": "/images/marco/01.png",
            "stories": [
                {"id": "s4", "imagen_url": "/images/marco/01.png", "texto": "Reunión de equipo 💪", "fecha": "2023-04-18"},
                {"id": "s5", "imagen_url": "/images/marco/contrato.png", "texto": "¡Proyecto entregado a tiempo! ✅🚀", "fecha": "2023-08-05"},
            ],
        },
    ],

    "reels": [
        {
            "id": "r1",
            "titulo": "Mi sitio favorito 📍",
            "miniatura_url": "https://images.mnstatic.com/fc/b3/fcb3e360a7e93529e6637062e9f23d06.jpg",
            "duracion": "0:45",
            "likes": 89,
            "comentarios": [
                {"usuario": "luisfer_22", "texto": "Trujillo siempre será hogar ❤️"},
            ],
        },
    ],

    "siguiendo": [
        {"id": "carlos", "username": "carlos.arenas_", "nombre": "Carlos Arenas", "foto_url": "/images/carlos/carlos_perfil.png"},
        {"id": "nexova", "username": "nexova_oficial", "nombre": "Nexova", "foto_url": "/images/nexova/nexova.jpg"},
        {"id": None, "username": "luisfer_22", "nombre": "Luis Fernando", "foto_url": "https://i.pinimg.com/736x/ce/99/8d/ce998d9b2dbff8bc1ccf3d48b5ebc845.jpg"},
        {"id": None, "username": "diego_sistemas", "nombre": "Diego Programador", "foto_url": "https://www.aprendemus.com/wp-content/uploads/2024/01/ingeniero-de-sistemas.jpg.webp"},
        {"id": None, "username": "jessica.m", "nombre": "Mamá Arenas", "foto_url": "/images/etc/pic02.jpg"},
        {"id": "camila", "username": "camila.a05", "nombre": "Camila Arenas", "foto_url": "/images/etc/pic01.jpg"},
    ],
}


# ────────────────────────────────────────────────────────────
# PERFIL 2 — Carlos Arenas (hermano)
# ────────────────────────────────────────────────────────────

PERFIL_CARLOS = {
    "id": "carlos",
    "username": "carlos.arenas_",
    "nombre": "Carlos Arenas",
    "foto_url": "/images/carlos/carlos_perfil.png",
    "bio": "Siempre en el medio 👨‍👩‍👧‍👦 | Visca el Barça | Amante de la fotografía 📸",
    "seguidores": 521,
    "publicaciones": 5,

    "posts": [
        {
            "id": "c1",
            "imagen_url": "/images/carlos/futbol.png",
            "caption": "Día de entrenamiento. Un día más cerca del sueño",
            "fecha": "2024-08-10",
            "likes": 43,
            "ubicacion": "Lima, Perú",
            "comentarios": [
                {"usuario": "luisfer_22", "texto": "¡Buenas fotos! ¿Quién las tomo?"},
                {"usuario": "camila.a05", "texto": "¡Yo! Con mi Nikon 📸"},
            ],
        },
        {
            "id": "c2",
            "imagen_url": "https://cloudfront-eu-central-1.images.arcpublishing.com/prisaradio/5ABWPBAJCVLDNH5UH672UCZLBQ.jpg",
            "caption": "Navidad con la familia Arenas completa 🎄👨‍👩‍👧‍👦 ¡Los 3 hermanos juntos como siempre! Bendiciones infinitas",
            "fecha": "2023-12-25",
            "likes": 92,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "La mejor navidad 🎄❤️"},
                {"usuario": "jessica.m", "texto": "Gracias Dios por mi familia 🙏"},
            ],
        },
        {
            "id": "c3",
            "imagen_url": "/images/carlos/carlos-rocky.png",
            "caption": "Cuidando al sobrino más peludo mientras mi hermano trabaja en Nexova 🐕❤️ Rocky es un amor de perro",
            "fecha": "2023-05-20",
            "likes": 54,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "Rocky te quiere mucho 🐕"},
            ],
        },
        {
            "id": "c4",
            "imagen_url": "/images/carlos/fiesta.jpg",
            "caption": "Hoy cumple años mi hermano @marco.arenas01 🎂🎉 Toca celebrar por todo lo alto",
            "fecha": "2022-03-15",
            "likes": 67,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "Gracias por la fiesta Carlos ❤️🎉"},
                {"usuario": "jessica.m", "texto": "Que Dios lo bendiga siempre 🙏❤️"},
            ],
        },
        {
            "id": "c5",
            "imagen_url": "/images/etc/jenga.jpg",
            "caption": "Domingo de familia con mis 2 hermanos favoritos 👨‍👩‍👧‍👦❤️ Los amo demasiado",
            "fecha": "2021-08-22",
            "likes": 85,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Los mejores domingos! ❤️"},
                {"usuario": "jessica.m", "texto": "Mis tres tesoros ❤️🙏"},
            ],
        },
    ],

    "historias_destacadas": [
        {
            "id": "chl1",
            "titulo": "Familia 👨‍👩‍👧‍👦",
            "portada_url": "https://portal.andina.pe/EDPFotografia3/thumbnail/2022/12/22/000920829M.jpg",
            "stories": [
                {"id": "cs1", "imagen_url": "https://portal.andina.pe/EDPFotografia3/thumbnail/2022/12/22/000920829M.jpg", "texto": "Almuerzo familiar de año nuevo ❤️", "fecha": "2023-01-01"},
                {"id": "cs2", "imagen_url": "https://cloudfront-eu-central-1.images.arcpublishing.com/prisaradio/5ABWPBAJCVLDNH5UH672UCZLBQ.jpg", "texto": "Los 3 hermanos Arenas reunidos 🎉", "fecha": "2023-12-25"},
            ],
        },
        {
            "id": "chl2",
            "titulo": "Trujillo 📍",
            "portada_url": "https://media.traveler.es/photos/62dd18bea031e21bace8385e/master/w_1600%2Cc_limit/GettyImages-694466288.jpg",
            "stories": [
                {"id": "cs3", "imagen_url": "https://media.traveler.es/photos/62dd18bea031e21bace8385e/master/w_1600%2Cc_limit/GettyImages-694466288.jpg", "texto": "Trujillo, la ciudad de la eterna primavera 🌸", "fecha": "2022-07-27"},
                {"id": "cs4", "imagen_url": "https://www.infobae.com/new-resizer/T7e3iUo4Jpl9z7pxqbhGAsG2kOY=/arc-anglerfish-arc2-prod-infobae/public/EA5E2RIHNVCGTNWMJBDZO5CHT4.jpg", "texto": "Atardecer en Huanchaco 🌅", "fecha": "2022-07-28"},
            ],
        },
    ],

    "siguiendo": [
        {"id": "marco", "username": "marco.arenas01", "nombre": "Marco Arenas", "foto_url": "/images/marco/marco_perfil.png"},
        {"id": "nexova", "username": "nexova_oficial", "nombre": "Nexova", "foto_url": "/images/nexova/nexova.jpg"},
        {"id": None, "username": "luisfer_22", "nombre": "Luis Fernando", "foto_url": "https://i.pinimg.com/736x/ce/99/8d/ce998d9b2dbff8bc1ccf3d48b5ebc845.jpg"},
        {"id": None, "username": "jessica.m", "nombre": "Mamá Arenas", "foto_url": "/images/etc/pic02.jpg"},
        {"id": "camila", "username": "camila.a05", "nombre": "Camila Arenas", "foto_url": "/images/etc/pic01.jpg"},
    ],
}

# ────────────────────────────────────────────────────────────
# PERFIL 3 — Nexova (empresa)
# ────────────────────────────────────────────────────────────

PERFIL_NEXOVA = {
    "id": "nexova",
    "username": "nexova_oficial",
    "nombre": "Nexova",
    "foto_url": "/images/nexova/nexova.jpg",
    "bio": "🏢 Soluciones tecnológicas innovadoras | 📍 Lima, Perú | 📧 Contacto: nexova.support@nexova.com | 🌐 www.nexova.com",
    "seguidores": 1240,
    "publicaciones": 5,

    "posts": [
        {
            "id": "n1",
            "imagen_url": "/images/nexova/images-1.jpg",
            "caption": "Nuevas oficinas, nuevo impulso 💪🏢 Renovamos nuestro espacio de trabajo en Trujillo para seguir creciendo e innovando. ¡Los esperamos!",
            "fecha": "2024-07-15",
            "likes": 89,
            "ubicacion": "Oficinas Nexova, Trujillo",
            "comentarios": [
                {"usuario": "luisfer_22", "texto": "¡Se ve genial la nueva oficina! 💼"},
            ],
        },
        {
            "id": "n2",
            "imagen_url": "/images/nexova/ani.jpg",
            "caption": "¡Nexova cumple 5 años! 🎂🎉 Cinco años transformando ideas en soluciones tecnológicas. Gracias a todo nuestro equipo y clientes por confiar en nosotros. #Nexova5Años",
            "fecha": "2024-03-01",
            "likes": 120,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Feliz aniversario Nexova! 🎉🚀"},
                {"usuario": "carlos.arenas_", "texto": "¡Felicidades! 🎂"},
            ],
        },
        {
            "id": "n3",
            "imagen_url": "/images/nexova/innova.jpg",
            "caption": "En Nexova seguimos innovando 💻🚀 ¿Necesitas una solución tecnológica para tu negocio? Contáctanos: nombre.apellido@nexova.com o visita nuestra web www.nexova.com",
            "fecha": "2023-11-20",
            "likes": 56,
            "comentarios": [
                {"usuario": "diego_sistemas", "texto": "¡Grandes soluciones! 💻"},
            ],
        },
        {
            "id": "n4",
            "imagen_url": "/images/nexova/integracion.jpg",
            "caption": "Evento de integración Nexova 2023 🎉💪 ¡Un equipo que trabaja unido, alcanza grandes metas! Gracias a todos los que hicieron posible este evento.",
            "fecha": "2023-06-15",
            "likes": 78,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Gran evento! 🚀"},
                {"usuario": "carlos.arenas_", "texto": "¡Se ve increíble! 👏"},
            ],
        },
        {
            "id": "n5",
            "imagen_url": "/images/nexova/inte.jpg",
            "caption": "¡Bienvenidos a los nuevos integrantes de Nexova! 🚀 Seguimos creciendo como equipo. Siempre buscamos talento que quiera transformar el futuro de la tecnología. #Nexova #Equipo #Trujillo",
            "fecha": "2023-02-01",
            "likes": 45,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Orgulloso de ser parte de este equipo! 💪"},
                {"usuario": "diego_sistemas", "texto": "¡Gran empresa! ¿Tienen vacantes? 👀"},
            ],
        },
    ],

    "historias_destacadas": [
        {
            "id": "nhl1",
            "titulo": "Proyectos 🚀",
            "portada_url": "https://i.pinimg.com/videos/thumbnails/originals/cd/61/00/cd6100bf8550c0cdfac6957348d14154.0000000.jpg",
            "stories": [
                {"id": "ns3", "imagen_url": "https://i.pinimg.com/videos/thumbnails/originals/cd/61/00/cd6100bf8550c0cdfac6957348d14154.0000000.jpg", "texto": "¡Otro proyecto exitoso entregado! ✅", "fecha": "2023-09-10"},
            ],
        },
    ],

    "reels": [
        {
            "id": "nr1",
            "titulo": "Un día en Nexova 💼",
            "miniatura_url": "/images/nexova/news.png",
            "duracion": "0:45",
            "likes": 95,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Así se trabaja en Nexova! 💪🚀"},
            ],
        },
    ],

    "siguiendo": [
        {"id": "marco", "username": "marco.arenas01", "nombre": "Marco Arenas", "foto_url": "/images/marco/marco_perfil.png"},
        {"id": "carlos", "username": "carlos.arenas_", "nombre": "Carlos Arenas", "foto_url": "/images/carlos/carlos_perfil.png"},
        {"id": None, "username": "luisfer_22", "nombre": "Luis Fernando", "foto_url": "https://i.pinimg.com/736x/ce/99/8d/ce998d9b2dbff8bc1ccf3d48b5ebc845.jpg"},
        {"id": None, "username": "diego_sistemas", "nombre": "Diego Programador", "foto_url": "https://www.aprendemus.com/wp-content/uploads/2024/01/ingeniero-de-sistemas.jpg.webp"},
    ],
}

# ────────────────────────────────────────────────────────────
# PERFIL 4 — Camila Arenas (hermana)
# ────────────────────────────────────────────────────────────

PERFIL_CAMILA = {
    "id": "camila",
    "username": "camila.a05",
    "nombre": "Camila Arenas",
    "foto_url": "/images/etc/pic01.jpg",
    "bio": "Fan de la música española | @cristina.ot2025 Ganadora",
    "seguidores": 4,
    "publicaciones": 1,

    "posts": [
        {
            "id": "ca1",
            "imagen_url": "/images/etc/foto01.jpg",
            "caption": "Foto del cielo en la playa",
            "fecha": "2021-08-22",
            "likes": 85,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡La mejor fotografa! ❤️"},
                {"usuario": "jessica.m", "texto": "Mi pequeña ❤️"},
            ],
        },
    ],

    "reels": [
        {
            "id": "cr1",
            "titulo": "Recorrido fotográfico por Trujillo 📸",
            "miniatura_url": "/images/etc/truj.webp",
            "duracion": "1:00",
            "likes": 2,
            "comentarios": [
                {"usuario": "marco.arenas01", "texto": "¡Qué buenas fotos tomas hermanita! 📸"},
            ],
        },
    ],

    "siguiendo": [
        {"id": "marco", "username": "marco.arenas01", "nombre": "Marco Arenas", "foto_url": "/images/marco/marco_perfil.png"},
        {"id": "carlos", "username": "carlos.arenas_", "nombre": "Carlos Arenas", "foto_url": "/images/carlos/carlos_perfil.png"},
        {"id": None, "username": "luisfer_22", "nombre": "Luis Fernando", "foto_url": "https://i.pinimg.com/736x/ce/99/8d/ce998d9b2dbff8bc1ccf3d48b5ebc845.jpg"},
        {"id": None, "username": "jessica.m", "nombre": "Mamá Arenas", "foto_url": "/images/etc/pic02.jpg"},
    ],
}