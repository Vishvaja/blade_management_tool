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

from sqlalchemy import text, extract

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_blades = db.execute(text("SELECT COUNT(*) FROM blades")).scalar()
    total_maintenances = db.execute(text("SELECT COUNT(*) FROM maintenance")).scalar()
    pending = db.execute(text("SELECT COUNT(*) FROM maintenance WHERE status = 'Pending'")).scalar()

    # Get current year dynamically
    current_year_query = text("""
        SELECT COUNT(DISTINCT blade_id)
        FROM maintenance
        WHERE EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
    """)
    maintained_this_year = db.execute(current_year_query).scalar()

    return {
        "totalBlades": total_blades or 0,
        "totalMaintenances": total_maintenances or 0,
        "pending": pending or 0,
        "maintainedThisYear": maintained_this_year or 0
    }


@router.get("/trends")
def get_maintenance_trends(db: Session = Depends(get_db)):
    status_counts = db.execute(text("SELECT status, COUNT(*) FROM maintenance GROUP BY status")).fetchall()
    issue_counts = db.execute(text("SELECT issue, COUNT(*) FROM maintenance GROUP BY issue")).fetchall()
    trend_data = db.execute(text("""
        SELECT TO_CHAR(date, 'Mon') AS month, COUNT(*)
        FROM maintenance
        WHERE date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY month
        ORDER BY MIN(date)
    """)).fetchall()

    return {
        "statusCounts": [{"status": row[0], "count": row[1]} for row in status_counts],
        "issueDistribution": [{"issue": row[0], "value": row[1]} for row in issue_counts],
        "monthlyTrend": [{"month": row[0], "count": row[1]} for row in trend_data],
    }

@router.get("/priority")
def get_priority_list(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT blade_id, issue, status, date, technician
        FROM maintenance
        WHERE status != 'Completed'
        ORDER BY status ASC, date ASC
        LIMIT 10
    """)).fetchall()

    return [
        {
            "bladeId": row[0],
            "issue": row[1],
            "status": row[2],
            "date": row[3].isoformat() if row[3] else None,
            "technician": row[4]
        }
        for row in rows
    ]

@router.get("/issues-by-site")
def get_issues_by_site(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT s.site_id, m.issue, COUNT(*)
        FROM maintenance m
        JOIN blades b ON m.blade_id = b.blade_id
        JOIN turbines t ON b.turbine_id = t.turbine_id
        JOIN sites s ON t.site_id = s.site_id
        GROUP BY s.site_id, m.issue
    """)).fetchall()
    result = {}
    for site_id, issue, count in rows:
        if site_id not in result:
            result[site_id] = {}
        result[site_id][issue] = count
    return result

@router.get("/technician-workload")
def get_technician_workload(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT technician, COUNT(*) FROM maintenance GROUP BY technician")).fetchall()
    return [{"technician": row[0], "count": row[1]} for row in rows]

@router.get("/technicians")
def get_technicians(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT DISTINCT technician FROM maintenance WHERE technician IS NOT NULL")).fetchall()
    return [row[0] for row in rows]

@router.get("/technicians/{technician_name}/maintenance")
def get_maintenance_by_technician(technician_name: str, db: Session = Depends(get_db)):
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
        }
        for row in rows
    ]

@router.get("/recurring-issues")
def get_recurring_issues(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT blade_id, issue, COUNT(*)
        FROM maintenance
        GROUP BY blade_id, issue
        HAVING COUNT(*) >= 2
    """)).fetchall()
    return [
        {"bladeId": row[0], "issue": row[1], "count": row[2]}
        for row in rows
    ]

@router.get("/problem-blades")
def get_problem_blades(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT blade_id, COUNT(*) as maintenance_count
        FROM maintenance
        GROUP BY blade_id
        ORDER BY maintenance_count DESC
        LIMIT 5
    """)).fetchall()
    return [
        {"bladeId": row[0], "maintenanceCount": row[1]}
        for row in rows
    ]

@router.get("/blades-due")
def get_blades_due_for_inspection(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT blade_id, MAX(date) as last_date
        FROM maintenance
        GROUP BY blade_id
        HAVING MAX(date) < CURRENT_DATE - INTERVAL '180 days'
    """)).fetchall()
    return [
        {"bladeId": row[0], "lastMaintained": row[1].isoformat() if row[1] else None}
        for row in rows
    ]
