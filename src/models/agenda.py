# src/models/agenda.py
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from src.models.user import Usuario


class ContactoBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=50)
    telefono: str = Field(schema_extra={"pattern": r"^\d{7,15}$"})
    mail: EmailStr


class Contacto(ContactoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Foreign Key hacia Usuario (Reto Práctico 2)
    user_id: Optional[int] = Field(default=None, foreign_key="usuario.id", index=True)
    propietario: Optional["Usuario"] = Relationship(back_populates="contactos")


class ContactoCreate(ContactoBase):
    pass


class ContactoUpdate(SQLModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    mail: Optional[EmailStr] = None
