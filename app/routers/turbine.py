from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import TurbineCreate, TurbineResponse, BladeResponse
from app.crud import crud
from app import database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[TurbineResponse])
def list_turbines(db: Session = Depends(get_db)):
    return crud.get_turbines(db)

@router.get("/{turbine_id}/blades", response_model=list[BladeResponse])
def blades_by_turbine(turbine_id: str, db: Session = Depends(get_db)):
    return crud.get_blades_by_turbine(db, turbine_id)

@router.post("", response_model=TurbineResponse)
def add_turbine(turbine: TurbineCreate, db: Session = Depends(get_db)):
    return crud.create_turbine(db, turbine)
