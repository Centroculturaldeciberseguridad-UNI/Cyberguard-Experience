import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import PROJECT_NAME, CORS_ORIGINS
from app.database import init_db
from app.usuarios_routes import router as usuarios_router
from app.ranking.routes import router as ranking_router
from app.retos.reto3_ReginaVi.routes import router as reto3_router
from app.retos.reto1_AlvaroCa.routes import router as reto1_router
from app.retos.reto2_MartinBe.routes import router as reto2_router

app = FastAPI(tittle=PROJECT_NAME, version="0.1.0")

# Comunicación backend con frontend de Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(usuarios_router)
app.include_router(ranking_router)
app.include_router(reto1_router)
app.include_router(reto2_router)
app.include_router(reto3_router)

@app.on_event("startup")
def startup():
    """Crea la carpeta de base de datos y las tablas al iniciar"""
    os.makedirs("database", exist_ok=True)
    init_db()

@app.get("/")
def root():
    return {"mensaje": f"Bienvenido a {PROJECT_NAME}"}

@app.get("/health")
def health():
    return {"status": "ok"}
