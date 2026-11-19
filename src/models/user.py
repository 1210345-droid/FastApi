# src/models/user.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from src.models.agenda import Contacto


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3)
    email: EmailStr
    hashed_password: str

    # Relación 1:N con Contacto (Reto Práctico 2)
    contactos: List["Contacto"] = Relationship(back_populates="propietario")


class UsuarioCreate(SQLModel):
    username: str
    email: EmailStr
    password: str


class UsuarioRead(SQLModel):
    id: int
    username: str
    email: EmailStr


class Token(SQLModel):
    access_token: str
    token_type: str
