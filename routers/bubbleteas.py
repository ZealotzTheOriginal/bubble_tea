from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import BubbleTeaDB
from schemas import BubbleTeaCreate, BubbleTeaResponse
from utils import filter_out_inactive_bubble_teas

# Creamos el router específico para Bubble Teas
# El 'prefix' hace que no tengamos que repetir "/bubbleteas" en cada endpoint
router = APIRouter(
    prefix="/bubbleteas",
    tags=["Bubble Teas"]
)

# 1. POST: Crear un nuevo Bubble Tea
@router.post("", response_model=BubbleTeaResponse, status_code=201)
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

# 2. GET Global: Obtener TODOS los Bubble Teas ACTIVOS
@router.get("", response_model=List[BubbleTeaResponse])
def get_bubble_teas(db: Session = Depends(get_db)):
    all_teas = db.query(BubbleTeaDB).all()
    return filter_out_inactive_bubble_teas(all_teas)

# 3. GET por ID: Obtener uno específico (Verifica que esté ACTIVO)
@router.get("/{tea_id}", response_model=BubbleTeaResponse)
def get_bubble_tea_by_id(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    
    if not tea or not tea.active:
        raise HTTPException(
            status_code=404, 
            detail="Bubble Tea no encontrado o no se encuentra activo"
        )
    return tea

# 4. PUT: Actualizar un Bubble Tea
@router.put("/{tea_id}", response_model=BubbleTeaResponse)
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

# 5. DELETE (Soft): Desactivar un Bubble Tea
@router.delete("/{tea_id}")
def soft_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")

    tea.active = False  
    db.commit()
    return {
        "message": f"Bubble Tea con ID {tea_id} ha sido deshabilitado (Soft Delete)."
    }

# 6. DELETE (Hard): Eliminar por completo
@router.delete("/{tea_id}/hard")
def hard_delete_bubble_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(BubbleTeaDB).filter(BubbleTeaDB.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Bubble Tea no encontrado")
    
    db.delete(tea)
    db.commit()
    return {"message": f"Bubble Tea con ID {tea_id} ha sido eliminado permanentemente."}