from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

# IMPORTACIONES DE SQLALCHEMY CORREGIDAS
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# =========================================================================
# 1. CONFIGURACIÓN DE LA BASE DE DATOS (SQLAlchemy)
# =========================================================================
# Reemplaza con tus credenciales reales: usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/tu_base_de_datos"

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
    price = Column(Decimal(5, 2), nullable=False)
    active = Column(Boolean, default=True) # TINYINT(1) se mapea como Boolean
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


# =========================================================================
# 3. ESQUEMAS DE VALIDACIÓN (Pydantic) - Equivalente al TypedDict del profe
# =========================================================================
class BubbleTeaResponse(BaseModel):
    id: int
    name: str
    temperature: str
    price: float
    active: bool

    class Config:
        from_attributes = True # Permite leer los datos directamente de SQLAlchemy

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

# Saludo de bienvenida (como el say_hello del profe)
@app.get("/")
def say_hello():
    return {"message": "¡Bienvenido a la API de Bubble Tea!"}


# --- ENDPOINTS PARA BUBBLE TEAS ---

# Obtener todos los Bubble Teas ACTIVOS (Filtro Soft Delete)
@app.get("/bubbleteas", response_model=List[BubbleTeaResponse])
def get_bubble_teas(db: Session = Depends(get_db)):
    # Aplicamos la misma lógica del ejercicio: filtrar solo los activos (active == 1)
    bubble_teas = db.query(BubbleTeaDB).filter(BubbleTeaDB.active == True).all()
    return bubble_teas


# Hacer un Soft Delete (Desactivar un Bubble Tea)
@app.delete("/bubbleteas/{tea_id}")
def soft_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")
    
    tea.active = False # Cambiamos el estado a 0 (Inactivo)
    db.commit()
    return {"message": f"Bubble Tea con ID {tea_id} ha sido eliminado (Soft Delete)."}


# --- ENDPOINTS PARA USUARIOS ---

# Obtener todos los usuarios
@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users