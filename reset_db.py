from app.database import Base, engine

def drop_and_recreate_all():
    print("⚠️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("🧹 All tables dropped.")

    print("📦 Recreating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Schema recreated successfully.")

if __name__ == "__main__":
    drop_and_recreate_all()
