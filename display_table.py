from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models

db: Session = SessionLocal()

sites = db.query(models.Site).all()
for site in sites:
    print(site.site_id, site.name, site.location)
