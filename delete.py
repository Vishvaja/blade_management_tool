from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models

# Start DB session
db: Session = SessionLocal()

# Find the maintenance record
record = db.query(models.Maintenance).filter(models.Maintenance.maintenance_id == 680).first()

if record:
    db.delete(record)
    db.commit()
    print("✅ Deleted maintenance_id 680 successfully.")
else:
    print("❌ maintenance_id 680 not found.")

# Always good to close the session
db.close()
