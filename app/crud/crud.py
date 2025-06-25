from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models import models
from app.schemas import schemas
from app.utils.utils import ensure_exists
# -----------------------------
# Sites
# -----------------------------

def get_sites(db: Session):
    return db.query(models.Site).all()

def create_site(db: Session, site: schemas.SiteCreate):
    db_site = models.Site(**site.dict())
    try:
        db.add(db_site)
        db.commit()
        db.refresh(db_site)
        return db_site
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Site with ID '{site.site_id}' already exists.")

# -----------------------------
# Turbines
# -----------------------------

def get_turbines(db: Session):
    return db.query(models.Turbine).all()

def get_turbines_by_site(db: Session, site_id: str):
    return db.query(models.Turbine).filter(models.Turbine.site_id == site_id).all()

def create_turbine(db: Session, turbine: schemas.TurbineCreate):
    ensure_exists(db, models.Site, "site_id", turbine.site_id, "Site")

    db_turbine = models.Turbine(**turbine.dict())
    try:
        db.add(db_turbine)
        db.commit()
        db.refresh(db_turbine)
        return db_turbine
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Turbine with ID '{turbine.turbine_id}' already exists.")

def update_turbine(db: Session, turbine_id: str, updates: schemas.TurbineUpdate):
    turbine = db.query(models.Turbine).filter_by(turbine_id=turbine_id).first()
    if not turbine:
        raise HTTPException(status_code=404, detail=f"❌ Turbine '{turbine_id}' not found.")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(turbine, key, value)
    db.commit()
    db.refresh(turbine)
    return turbine

# -----------------------------
# Blades
# -----------------------------

def get_blades(db: Session):
    return db.query(models.Blade).all()

def get_blades_by_turbine(db: Session, turbine_id: str):
    return db.query(models.Blade).filter(models.Blade.turbine_id == turbine_id).all()

def create_blade(db: Session, blade: schemas.BladeCreate):
    ensure_exists(db, models.Turbine, "turbine_id", blade.turbine_id, "Turbine")
    db_blade = models.Blade(**blade.dict())
    try:
        db.add(db_blade)
        db.commit()
        db.refresh(db_blade)
        return db_blade
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Blade with ID '{blade.blade_id}' already exists.")

def update_blade(db: Session, blade_id: str, updates: schemas.BladeUpdate):
    blade = db.query(models.Blade).filter_by(blade_id=blade_id).first()
    if not blade:
        raise HTTPException(status_code=404, detail=f"❌ Blade '{blade_id}' not found.")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(blade, key, value)
    db.commit()
    db.refresh(blade)
    return blade
# -----------------------------
# Maintenance
# -----------------------------

def get_maintenance_records(db: Session):
    return db.query(models.Maintenance).all()

def get_maintenance_by_blade(db: Session, blade_id: str):
    return db.query(models.Maintenance).filter(models.Maintenance.blade_id == blade_id).all()

def create_maintenance(db: Session, entry: schemas.MaintenanceCreate):
    ensure_exists(db, models.Blade, "blade_id", entry.blade_id, "Blade")
    db_entry = models.Maintenance(**entry.dict())
    try:
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"❌ Duplicate maintenance record or foreign key constraint failed.")

def update_maintenance(db: Session, maintenance_id: int, updates: schemas.MaintenanceUpdate):
    record = db.query(models.Maintenance).filter_by(maintenance_id=maintenance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"❌ Maintenance record ID '{maintenance_id}' not found.")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record
