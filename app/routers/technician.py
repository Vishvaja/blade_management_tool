from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. /technicians -> list of all unique technician names
@router.get("/technicians")
def get_technicians(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT DISTINCT technician FROM maintenance
        WHERE technician IS NOT NULL
    """)).fetchall()
    return [row[0] for row in rows]

# 2. /technician-workload -> count of tasks per technician
@router.get("/technician-workload")
def get_technician_workload(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT technician, COUNT(*) as task_count 
        FROM maintenance
        WHERE technician IS NOT NULL
        GROUP BY technician
    """)).fetchall()
    return [{"technician": row[0], "count": row[1]} for row in rows]

# 3. /technicians/{technician}/maintenance
@router.get("/technicians/{technician_name}/maintenance")
def get_technician_maintenance(technician_name: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT blade_id, issue, status, date 
        FROM maintenance 
        WHERE technician = :technician
        ORDER BY date DESC
    """), {"technician": technician_name}).fetchall()
    return [
        {
            "bladeId": row[0],
            "issue": row[1],
            "status": row[2],
            "date": row[3].isoformat() if row[3] else None
        } for row in rows
    ]

# 4. /all-maintenance
@router.get("/all-maintenance")
def get_all_maintenance(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT technician, blade_id, issue, status, date 
        FROM maintenance
        ORDER BY date DESC
    """)).fetchall()
    return [
        {
            "technician": row[0],
            "bladeId": row[1],
            "issue": row[2],
            "status": row[3],
            "date": row[4].isoformat() if row[4] else None
        } for row in rows
    ]

# 5. /status-counts -> status-wise count for all technicians
@router.get("/status-counts")
def get_status_counts(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT status, COUNT(*) 
        FROM maintenance
        WHERE technician IS NOT NULL
        GROUP BY status
    """)).fetchall()
    return [{"status": row[0], "count": row[1]} for row in rows]

# 6. /technicians/{technician}/issues -> issue-wise count for radar chart
@router.get("/technicians/{technician_name}/issues")
def get_technician_issues(technician_name: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT issue, COUNT(*) 
        FROM maintenance
        WHERE technician = :technician
        GROUP BY issue
    """), {"technician": technician_name}).fetchall()
    return [{"issue": row[0], "count": row[1]} for row in rows]

# 7. /technicians/{technician}/trend -> trend of maintenance counts over months
@router.get("/technicians/{technician_name}/trend")
def get_technician_trend(technician_name: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT TO_CHAR(date, 'YYYY-MM') AS month, COUNT(*)
        FROM maintenance
        WHERE technician = :technician
        GROUP BY month
        ORDER BY month
    """), {"technician": technician_name}).fetchall()
    return [{"month": row[0], "count": row[1]} for row in rows]

# 8. /technicians/{technician}/status-counts -> status-wise count for specific technician
@router.get("/technicians/{technician_name}/status-counts")
def get_status_counts_for_technician(technician_name: str, db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT status, COUNT(*) 
        FROM maintenance
        WHERE technician = :technician
        GROUP BY status
    """), {"technician": technician_name}).fetchall()
    
    return [{"status": row[0], "count": row[1]} for row in rows]

@router.get("/technicians/status-summary")
def get_overall_status_summary(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT status, COUNT(*) 
        FROM maintenance
        GROUP BY status
    """)).fetchall()

    return {row[0]: row[1] for row in rows}

@router.get("/technicians/summary")
def get_technician_summary(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT technician, COUNT(*) 
        FROM maintenance
        WHERE technician IS NOT NULL
        GROUP BY technician
    """)).fetchall()

    return [{"technician": row[0], "count": row[1]} for row in rows]
