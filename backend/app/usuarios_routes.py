from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro", response_model=UsuarioResponse)
def registrar_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo nickname (3-30 caracteres, solo letras/números/guiones, único)."""
    nickname = data.nickname.strip()

    existente = db.query(Usuario).filter(Usuario.nickname == nickname).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ese nickname ya está en uso.")

    usuario = Usuario(nickname=nickname)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.get("/{nickname}", response_model=UsuarioResponse)
def obtener_usuario(nickname: str, db: Session = Depends(get_db)):
    """Obtiene un usuario existente por nickname."""
    usuario = db.query(Usuario).filter(Usuario.nickname == nickname).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario