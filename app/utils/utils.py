from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def ensure_exists(db, model, key_field: str, value: str, entity_name: str):
    if not db.query(model).filter(getattr(model, key_field) == value).first():
        raise HTTPException(status_code=400, detail=f"❌ {entity_name} '{value}' does not exist.")
