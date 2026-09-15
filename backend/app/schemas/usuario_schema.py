import re
from pydantic import BaseModel, field_validator

class UsuarioCreate(BaseModel):
    nickname: str

    @field_validator("nickname")
    @classmethod
    def validar_nickname(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3 or len(v) > 30:
            raise ValueError("El nickname debe tener entre 3 y 30 caracteres.")
        if not re.match(r"^[a-zA-Z0-9\-]+$", v):
            raise ValueError("El nickname solo puede contener letras, números y guiones.")
        return v

class UsuarioResponse(BaseModel):
    id: int
    nickname: str

    model_config = {"from_attributes": True}
