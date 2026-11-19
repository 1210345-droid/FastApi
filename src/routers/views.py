# src/routers/views.py
from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlmodel import Session, select
from src.database import get_session
from src.models.agenda import Contacto, ContactoCreate

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(prefix="/views", tags=["Vistas Web (Jinja2)"])


@router.get("/agenda")
def render_agenda_view(request: Request, session: Session = Depends(get_session)):
    contactos = session.exec(select(Contacto)).all()
    # Obligatorio pasar "request" en el diccionario de contexto de Jinja2
    return templates.TemplateResponse(
        request=request,
        name="agenda.html",
        context={"contactos": contactos},
    )


@router.post("/agenda")
def create_agenda_from_form(
    request: Request,
    nombre: str = Form(...),
    telefono: str = Form(...),
    mail: str = Form(...),
    session: Session = Depends(get_session),
):
    """Procesa el formulario HTML en Jinja2 para agregar nuevos contactos (Reto Práctico 3)."""
    try:
        contacto_in = ContactoCreate(nombre=nombre, telefono=telefono, mail=mail)
        nuevo = Contacto.model_validate(contacto_in)
        session.add(nuevo)
        session.commit()
        return RedirectResponse(
            url="/views/agenda", status_code=status.HTTP_303_SEE_OTHER
        )
    except ValidationError as exc:
        contactos = session.exec(select(Contacto)).all()
        return templates.TemplateResponse(
            request=request,
            name="agenda.html",
            context={
                "contactos": contactos,
                "error": f"Datos inválidos: {exc.errors()[0]['msg']}",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
