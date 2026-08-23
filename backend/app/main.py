# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import init_db
from app.api.endpoints import router as research_router

app = FastAPI(
    title="Research Intelligence & Paper Engineering API",
    version="1.0.0",
    description="Backend API powering research discovery, gap analysis, and paper engineering.",
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(research_router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "Resonance AI API running"}