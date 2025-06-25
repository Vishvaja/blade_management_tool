from fastapi import FastAPI
from app.routers import site, turbine, blade, maintenance,dashboard,technician
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)
app = FastAPI()

# Allow React dev server to access FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, etc.
    allow_headers=["*"],
)

app.include_router(site.router, prefix="/sites", tags=["Sites"])
app.include_router(turbine.router, prefix="/turbines", tags=["Turbines"])
app.include_router(blade.router, prefix="/blades", tags=["Blades"])
app.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(technician.router,prefix="/api/technician", tags=["Technician"])