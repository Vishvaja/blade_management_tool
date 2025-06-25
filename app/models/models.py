from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Site(Base):
    __tablename__ = "sites"
    site_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    turbines = relationship("Turbine", back_populates="site")

class Turbine(Base):
    __tablename__ = "turbines"
    turbine_id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.site_id"))
    model = Column(String)
    site = relationship("Site", back_populates="turbines")
    blades = relationship("Blade", back_populates="turbine")

class Blade(Base):
    __tablename__ = "blades"
    blade_id = Column(String, primary_key=True, index=True)
    turbine_id = Column(String, ForeignKey("turbines.turbine_id"))
    type = Column(String)
    length = Column(Integer)
    turbine = relationship("Turbine", back_populates="blades")
    maintenance = relationship("Maintenance", back_populates="blade")

class Maintenance(Base):
    __tablename__ = "maintenance"
    maintenance_id = Column(Integer, primary_key=True, index=True)
    blade_id = Column(String, ForeignKey("blades.blade_id"))
    date = Column(Date)
    status = Column(String)
    issue = Column(Text)
    technician = Column(String)
    blade = relationship("Blade", back_populates="maintenance")
