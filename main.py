import os
from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, Numeric, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# NUEVO: Importar cargador de variables de entorno
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# =========================================================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS (Cargada desde .env)
# =========================================================================
# Intenta leer DATABASE_URL del .env; si no existe, usa una por defecto para evitar caídas.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "ERROR: No se encontró la variable DATABASE_URL en el archivo .env"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependencia para obtener la sesión de la base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================================
# 2. MODELOS DE LAS TABLAS (SQLAlchemy ORM)
# =========================================================================
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class BubbleTeaDB(Base):
    __tablename__ = "bubble_teas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    temperature = Column(String(20), nullable=False)
    price = Column(Numeric(5, 2), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


# =========================================================================
# 3. ESQUEMAS DE VALIDACIÓN (Pydantic)
# =========================================================================
class BubbleTeaResponse(BaseModel):
    id: int
    name: str
    temperature: str
    price: float
    active: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    class Config:
        from_attributes = True


# =========================================================================
# 4. INSTANCIA DE FASTAPI Y ENDPOINTS
# =========================================================================
app = FastAPI(title="Bubble Tea & Users API")


@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}


# --- FUNCIONES AUXILIARES DE FILTRADO ---
def filter_out_inactive_bubble_teas(db_teas: List[BubbleTeaDB]) -> List[BubbleTeaDB]:
    return [tea for tea in db_teas if tea.active]


# --- ENDPOINTS PARA BUBBLE TEAS ---


# Obtener todos los Bubble Teas ACTIVOS
@app.get("/bubbleteas", response_model=List[BubbleTeaResponse])
def get_bubble_teas(db: Session = Depends(get_db)):
    all_teas = db.query(BubbleTeaDB).all()
    return filter_out_inactive_bubble_teas(all_teas)


# Hacer un Soft Delete (Desactivar un Bubble Tea)
@app.delete("/bubbleteas/{tea_id}")
def soft_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")

    tea.active = False  # Cambiamos el estado a 0
    db.commit()
    return {
        "message": f"Bubble Tea con ID {tea_id} ha sido eliminado (Soft Delete)."
    }


# --- ENDPOINTS PARA USUARIOS ---


# Obtener todos los usuarios
@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users