from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from app.schemas.schemas import BladeCreate, BladeResponse, BladeUpdate, MaintenanceResponse
from app.crud import crud
from app import database
from app.models.models import Blade

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[BladeResponse])
async def list_blades(db: Session = Depends(get_db)):
    blades = db.query(Blade).options(joinedload(Blade.maintenance)).all()
    return blades


@router.get("/{blade_id}/maintenance", response_model=list[MaintenanceResponse])
def maintenance_by_blade(blade_id: str, db: Session = Depends(get_db)):
    return crud.get_maintenance_by_blade(db, blade_id)

@router.post("", response_model=BladeResponse)
def add_blade(blade: BladeCreate, db: Session = Depends(get_db)):
    return crud.create_blade(db, blade)

@router.put("/{blade_id}", response_model=BladeResponse)
def edit_blade(blade_id: str, updates: BladeUpdate, db: Session = Depends(get_db)):
    blade = crud.update_blade(db, blade_id, updates)
    if not blade:
        raise HTTPException(status_code=404, detail="Blade not found")
    return blade
