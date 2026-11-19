# src/config.py
import os

SECRET_KEY: str = os.getenv(
    "SECRET_KEY", "CAMBIAR_ESTA_LLAVE_SECRETA_SUPER_SEGURA_EN_PRODUCCION"
)
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./agenda.db")
