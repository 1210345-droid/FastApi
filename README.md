# Sistema de Agenda Empresarial (FastAPI Profesional)

Aplicación backend modular construida con **FastAPI**, **SQLModel**, **OAuth2 / JWT**, **Middlewares** y **Jinja2 (SSR)** siguiendo el Manual de Cátedra e incluyendo los **3 Retos Prácticos**.

---

## Estructura del Proyecto

```text
mi_agenda_fastapi/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Variables de entorno y llaves secretas
│   ├── database.py               # Engine, sesión e inicialización con SQLModel
│   ├── models/                   # Tablas y esquemas de validación
│   │   ├── __init__.py
│   │   ├── user.py               # Modelo de Usuario y Auth (Relación 1:N con Contacto)
│   │   └── agenda.py             # Modelo SQLModel de Contactos (con user_id Foreign Key)
│   ├── auth/                     # Lógica de seguridad y tokens
│   │   ├── __init__.py
│   │   ├── security.py           # Hash de contraseñas (Bcrypt) y creación de JWT
│   │   └── dependencies.py       # Dependencia get_current_user con OAuth2
│   ├── routers/                  # Controladores / Endpoints REST
│   │   ├── __init__.py
│   │   ├── auth.py               # Login (/auth/token) y Registro (/auth/register)
│   │   ├── agenda.py             # CRUD protegido de Contactos filtrado por usuario
│   │   └── views.py              # Rutas HTML con Jinja2 (GET y POST desde formulario)
│   ├── middlewares/              # Middlewares HTTP
│   │   ├── __init__.py
│   │   └── timer.py              # Medición de tiempo de ejecución (X-Process-Time)
│   └── templates/                # Plantillas HTML Jinja2
│       ├── base.html
│       └── agenda.html           # Tabla y formulario web para agregar contactos
├── static/                       # Archivos CSS/JS públicos
├── main.py                       # Orquestador y punto de entrada
└── requirements.txt
```

---

## Instalación y Ejecución

1. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Iniciar el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```
4. Accesos rápidos:
   - **API Root**: http://127.0.0.1:8000/
   - **Swagger UI**: http://127.0.0.1:8000/docs
   - **Panel Web Jinja2**: http://127.0.0.1:8000/views/agenda

---

## Solución a los 3 Retos Prácticos

### Reto 1: Prueba Swagger de OAuth2 (`/docs`)
1. Abre la documentación interactiva en `http://127.0.0.1:8000/docs`.
2. Despliega el endpoint `POST /auth/register`, haz clic en **Try it out** y registra un usuario:
   ```json
   {
     "username": "alumno1",
     "email": "alumno1@universidad.edu",
     "password": "MiPasswordSeguro123"
   }
   ```
3. Si intentas ejecutar `GET /agenda`, `POST /agenda`, `PUT /agenda/{id}` o `DELETE /agenda/{id}` sin autenticarte, recibirás un código `401 Unauthorized` con el detalle `"Not authenticated"`.
4. Haz clic en el botón verde **Authorize** (con ícono de candado) en la esquina superior derecha de `/docs`.
5. En el formulario modal (`OAuth2PasswordBearer`), ingresa:
   - **username**: `alumno1`
   - **password**: `MiPasswordSeguro123`
6. Haz clic en **Authorize** y luego en **Close**.
7. Ahora Swagger adjuntará automáticamente el header `Authorization: Bearer <access_token>` en cada petición a `/agenda`, permitiendo crear, listar, actualizar y eliminar tus contactos sin error `401`.

### Reto 2: Relación de Tablas (`user_id` Foreign Key)
- En `src/models/agenda.py`, el modelo `Contacto` incluye:
  ```python
  user_id: Optional[int] = Field(default=None, foreign_key="usuario.id", index=True)
  propietario: Optional["Usuario"] = Relationship(back_populates="contactos")
  ```
- En `src/models/user.py`, el modelo `Usuario` declara la relación inversa:
  ```python
  contactos: List["Contacto"] = Relationship(back_populates="propietario")
  ```
- En `src/routers/agenda.py`, todas las operaciones filtran por `Contacto.user_id == current_user.id`, garantizando que cada usuario autenticado solo pueda ver, crear, editar y eliminar sus propios contactos.

### Reto 3: Formulario HTML en Jinja2
- En `src/templates/agenda.html`, se incluyó una tarjeta lateral con un formulario `<form action="/views/agenda" method="post">` con validación HTML5 para `nombre`, `telefono` y `mail`.
- En `src/routers/views.py`, el endpoint `POST /views/agenda` recibe los campos mediante `Form(...)` (gracias a `python-multipart`), valida los datos con `ContactoCreate`, inserta el registro en SQLite y redirige a `/views/agenda` (`303 See Other`).
