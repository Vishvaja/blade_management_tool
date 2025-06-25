from pydantic import BaseModel
from typing import Optional,List
from datetime import date

# -----------------------------
# Site Schemas
# -----------------------------

class TopSiteStats(BaseModel):
    site_id: str
    name: str
    total: int

class SiteBase(BaseModel):
    site_id: str
    name: str
    location: str

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    class Config:
        orm_mode = True


# -----------------------------
# Turbine Schemas
# -----------------------------

class TurbineBase(BaseModel):
    turbine_id: str
    site_id: str
    model: str

class TurbineCreate(TurbineBase):
    pass

class TurbineUpdate(BaseModel):
    model: Optional[str] = None
    site_id: Optional[str] = None  # optional if you want to allow reassignment

class TurbineResponse(TurbineBase):
    class Config:
        orm_mode = True
        
# -----------------------------
# Maintenance Schemas
# -----------------------------

class MaintenanceBase(BaseModel):
    blade_id: str
    date: date
    status: str
    issue: str
    technician: str

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    status: Optional[str] = None
    issue: Optional[str] = None
    technician: Optional[str] = None

class MaintenanceResponse(BaseModel):
    maintenance_id: int
    blade_id: str
    date: date
    status: str
    issue: str
    technician: str

    class Config:
        orm_mode = True

# -----------------------------
# Blade Schemas
# -----------------------------

class BladeBase(BaseModel):
    blade_id: str
    turbine_id: str
    type: str
    length: int

class BladeCreate(BladeBase):
    pass

class BladeUpdate(BaseModel):
    type: Optional[str] = None
    length: Optional[int] = None

class BladeResponse(BaseModel):
    blade_id: str
    turbine_id: str
    type: str
    length: int
    maintenance: List[MaintenanceResponse] = []  # ✅ Include related maintenance records

    class Config:
        orm_mode = True




