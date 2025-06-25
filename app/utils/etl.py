import pandas as pd
from sqlalchemy.orm import Session
from app.models import models
from app import database
import logging
import os

# Setup logging
logging.basicConfig(filename="etl.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(value):
    if isinstance(value, str):
        return value.strip().title()
    return value

def load_sites(csv_path: str, db: Session):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=['site_id', 'site_name', 'location'])

    count, seen_ids, duplicates = 0, set(), []

    for _, row in df.iterrows():
        site_id = str(row['site_id']).strip().upper()
        if site_id in seen_ids:
            duplicates.append(site_id)
            continue
        seen_ids.add(site_id)

        site = models.Site(
            site_id=site_id,
            name=clean_text(row['site_name']),
            location=clean_text(row['location'])
        )
        try:
            db.merge(site)
            count += 1
        except Exception as e:
            db.rollback()
            logging.warning(f"⚠️ Error inserting site_id={site_id}: {e}")

    db.commit()
    logging.info(f"✅ Sites loaded: {count}")
    if duplicates:
        logging.warning(f"🚫 Skipped duplicate site_id(s): {set(duplicates)}")

def load_turbines(csv_path: str, db: Session):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=['turbine_id', 'site_id', 'turbine_model'])

    count, seen_ids, duplicates = 0, set(), []

    for _, row in df.iterrows():
        turbine_id = str(row['turbine_id']).strip().upper()
        site_id = str(row['site_id']).strip().upper()

        if turbine_id in seen_ids:
            duplicates.append(turbine_id)
            continue
        seen_ids.add(turbine_id)

        if not db.query(models.Site).filter_by(site_id=site_id).first():
            logging.warning(f"⛔ Skipping turbine: unknown site_id '{site_id}'")
            continue

        turbine = models.Turbine(
            turbine_id=turbine_id,
            site_id=site_id,
            model=clean_text(row['turbine_model'])
        )
        try:
            db.merge(turbine)
            count += 1
        except Exception as e:
            db.rollback()
            logging.warning(f"⚠️ Error inserting turbine_id={turbine_id}: {e}")

    db.commit()
    logging.info(f"✅ Turbines loaded: {count}")
    if duplicates:
        logging.warning(f"🚫 Skipped duplicate turbine_id(s): {set(duplicates)}")

def load_blades(csv_path: str, db: Session):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=['blade_id', 'turbine_id', 'blade_type', 'length_m'])

    count, seen_ids, duplicates = 0, set(), []

    for _, row in df.iterrows():
        blade_id = str(row['blade_id']).strip().upper()
        turbine_id = str(row['turbine_id']).strip().upper()

        if blade_id in seen_ids:
            duplicates.append(blade_id)
            continue
        seen_ids.add(blade_id)

        if not db.query(models.Turbine).filter_by(turbine_id=turbine_id).first():
            logging.warning(f"⛔ Skipping blade: unknown turbine_id '{turbine_id}'")
            continue

        blade = models.Blade(
            blade_id=blade_id,
            turbine_id=turbine_id,
            type=clean_text(row['blade_type']),
            length=int(row['length_m'])
        )
        try:
            db.merge(blade)
            count += 1
        except Exception as e:
            db.rollback()
            logging.warning(f"⚠️ Error inserting blade_id={blade_id}: {e}")

    db.commit()
    logging.info(f"✅ Blades loaded: {count}")
    if duplicates:
        logging.warning(f"🚫 Skipped duplicate blade_id(s): {set(duplicates)}")

def load_maintenance(csv_path: str, db: Session):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.dropna(subset=['blade_id', 'date', 'repair_status', 'issue_found', 'technician'])

    count, seen_keys, duplicates = 0, set(), []

    for _, row in df.iterrows():
        blade_id = str(row['blade_id']).strip().upper()
        date_key = pd.to_datetime(row['date']).date()
        key = (blade_id, date_key)

        if key in seen_keys:
            duplicates.append(key)
            continue
        seen_keys.add(key)

        if not db.query(models.Blade).filter_by(blade_id=blade_id).first():
            logging.warning(f"⛔ Skipping maintenance: unknown blade_id '{blade_id}'")
            continue

        entry = models.Maintenance(
            blade_id=blade_id,
            date=date_key,
            status=clean_text(row['repair_status']),
            issue=clean_text(row['issue_found']),
            technician=clean_text(row['technician'])
        )
        try:
            db.add(entry)
            count += 1
        except Exception as e:
            db.rollback()
            logging.warning(f"⚠️ Error inserting maintenance for blade_id={blade_id}: {e}")

    db.commit()
    logging.info(f"✅ Maintenance records loaded: {count}")
    if duplicates:
        logging.warning(f"🚫 Skipped duplicate maintenance entries: {len(duplicates)}")

# ---------- Entry Point ----------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")  # adjust path if needed

def run_all():
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)

    db = database.SessionLocal()
    try:
        load_sites(os.path.join(DATA_PATH, "Site Table.csv"), db)
        load_turbines(os.path.join(DATA_PATH, "Turbines and Blades.csv"), db)
        load_blades(os.path.join(DATA_PATH, "Blade Table.csv"), db)
        load_maintenance(os.path.join(DATA_PATH, "Blade Maintenance.csv"), db)
    finally:
        db.close()
