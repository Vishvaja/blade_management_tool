from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from app.schemas.schemas import SiteCreate, SiteResponse, TopSiteStats,TurbineCreate, TurbineResponse
from collections import defaultdict
from app.crud import crud
from app import database
from app.models.models import Maintenance, Site,Blade,Turbine

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[SiteResponse])
def list_sites(db: Session = Depends(get_db)):
    return crud.get_sites(db)

@router.post("", response_model=SiteResponse)
def add_site(site: SiteCreate, db: Session = Depends(get_db)):
    return crud.create_site(db, site)

@router.get("/{site_id}/turbines", response_model=list[TurbineResponse])
def turbines_by_site(site_id: str, db: Session = Depends(get_db)):
    return crud.get_turbines_by_site(db, site_id)

@router.get("/top_sites_by_maintenance", response_model=list[TopSiteStats])
def top_sites_by_maintenance(db: Session = Depends(get_db)):
    # Load all relationships via joins
    maints = db.query(Maintenance).join(Blade).join(Turbine).join(Site).options(
        joinedload(Maintenance.blade).joinedload(Blade.turbine).joinedload(Turbine.site)
    ).all()

    count_map = defaultdict(int)

    for m in maints:
        site_id = m.blade.turbine.site.site_id
        count_map[site_id] += 1

    site_names = {
        s.site_id: s.name for s in db.query(Site).all()
    }

    top_sites = sorted(
        [{"site_id": sid, "name": site_names.get(sid, sid), "total": count}
         for sid, count in count_map.items()],
        key=lambda x: x["total"],
        reverse=True
    )[:5]

    return top_sites
