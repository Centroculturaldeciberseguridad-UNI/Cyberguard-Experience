import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Conjunto de rutas base
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent
DATABASE_DIR = BACKEND_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

# Configuración general
PROJECT_NAME = os.getenv("PROJECT_NAME", "CyberGuard Experience")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_DIR / 'ciberseguridad.db'}"
)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
