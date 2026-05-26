from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# Importaciones locales de los otros archivos que acabamos de crear
from database import get_db
from models import BubbleTeaDB, UserDB
from schemas import BubbleTeaCreate, BubbleTeaResponse, UserResponse
from utils import filter_out_inactive_bubble_teas

app = FastAPI(title="Bubble Tea & Users API")

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

# =========================================================================
# ENDPOINTS PARA BUBBLE TEAS
# =========================================================================

# 1. POST: Crear un nuevo Bubble Tea en Aiven
@app.post("/bubbleteas", response_model=BubbleTeaResponse, status_code=201)
def create_bubble_tea(tea_data: BubbleTeaCreate, db: Session = Depends(get_db)):
    nuevo_tea = BubbleTeaDB(
        name=tea_data.name,
        temperature=tea_data.temperature,
        price=tea_data.price,
        active=tea_data.active
    )
    db.add(nuevo_tea)
    db.commit()
    db.refresh(nuevo_tea)
    return nuevo_tea


# 2. GET Global: Obtener TODOS los Bubble Teas ACTIVOS de Aiven
@app.get("/bubbleteas", response_model=List[BubbleTeaResponse])
def get_bubble_teas(db: Session = Depends(get_db)):
    all_teas = db.query(BubbleTeaDB).all()
    return filter_out_inactive_bubble_teas(all_teas)


# 3. GET por ID: Obtener uno específico de Aiven (Verifica que esté ACTIVO)
@app.get("/bubbleteas/{tea_id}", response_model=BubbleTeaResponse)
def get_bubble_tea_by_id(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    
    if not tea or not tea.active:
        raise HTTPException(
            status_code=404, 
            detail="Bubble Tea no encontrado o no se encuentra activo"
        )
    return tea


# 4. PUT: Actualizar un Bubble Tea en Aiven
@app.put("/bubbleteas/{tea_id}", response_model=BubbleTeaResponse)
def update_bubble_tea(tea_id: int, tea_data: BubbleTeaCreate, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")
    
    tea.name = tea_data.name
    tea.temperature = tea_data.temperature
    tea.price = tea_data.price
    tea.active = tea_data.active
    
    db.commit()
    db.refresh(tea)
    return tea


# 5. DELETE (Soft): Desactivar un Bubble Tea en Aiven
@app.delete("/bubbleteas/{tea_id}")
def soft_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")

    tea.active = False  
    db.commit()
    return {
        "message": f"Bubble Tea con ID {tea_id} ha sido deshabilitado (Soft Delete)."
    }


# 6. DELETE (Hard): Eliminar por completo de Aiven
@app.delete("/bubbleteas/{tea_id}/hard")
def hard_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")
    
    db.delete(tea)
    db.commit()
    return {"message": f"Bubble Tea con ID {tea_id} ha sido eliminado permanentemente."}


# =========================================================================
# ENDPOINTS PARA USUARIOS
# =========================================================================

@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users