from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.crud import crud
from app import database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[MaintenanceResponse])
def list_maintenance(db: Session = Depends(get_db)):
    return crud.get_maintenance_records(db)

@router.post("", response_model=MaintenanceResponse)
def add_maintenance(entry: MaintenanceCreate, db: Session = Depends(get_db)):
    return crud.create_maintenance(db, entry)

@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance_entry(maintenance_id: int, updates: MaintenanceUpdate, db: Session = Depends(get_db)):
    record = crud.update_maintenance(db, maintenance_id, updates)
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return record
