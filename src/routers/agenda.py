# src/routers/agenda.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database import get_session
from src.models.agenda import Contacto, ContactoCreate, ContactoUpdate
from src.models.user import Usuario
from src.auth.dependencies import get_current_user

router = APIRouter(prefix="/agenda", tags=["Agenda CRUD"])


@router.get("", response_model=List[Contacto])
def get_contactos(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Lista únicamente los contactos que pertenecen al usuario autenticado (Reto 2)."""
    statement = select(Contacto).where(Contacto.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/{id}", response_model=Contacto)
def get_contacto(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Obtiene un contacto por ID validando que pertenezca al usuario autenticado."""
    contacto = session.get(Contacto, id)
    if not contacto or contacto.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacto no encontrado"
        )
    return contacto


@router.post("", response_model=Contacto, status_code=status.HTTP_201_CREATED)
def crear_contacto(
    contacto_in: ContactoCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),  # Ruta protegida con JWT
):
    """Crea un contacto vinculándolo con user_id del usuario autenticado."""
    nuevo = Contacto.model_validate(
        contacto_in, update={"user_id": current_user.id}
    )
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=Contacto)
def actualizar_contacto(
    id: int,
    contacto_in: ContactoUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),  # Ruta protegida con JWT
):
    """Actualiza un contacto solo si pertenece al usuario autenticado."""
    contacto_db = session.get(Contacto, id)
    if not contacto_db or contacto_db.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")

    update_data = contacto_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contacto_db, key, value)

    session.add(contacto_db)
    session.commit()
    session.refresh(contacto_db)
    return contacto_db


@router.delete("/{id}")
def eliminar_contacto(
    id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),  # Ruta protegida con JWT
):
    """Elimina un contacto solo si pertenece al usuario autenticado."""
    contacto = session.get(Contacto, id)
    if not contacto or contacto.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    session.delete(contacto)
    session.commit()
    return {
        "mensaje": f"Contacto {id} eliminado correctamente por @{current_user.username}"
    }
