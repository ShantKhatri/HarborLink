from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pathlib import Path
import uvicorn

from .api.routes import api_router
from .db.database import engine, Base
from app.api.endpoints import projects
print("Projects router endpoints:", [route.path for route in projects.router.routes])
print("API router endpoints:", [route.path for route in api_router.routes])

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HarborLink",
    description="AI-Powered Middleware for ONDC/OCEN API Compliance",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)

frontend_build = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_build):
    for item in os.listdir(frontend_build):
        src = os.path.join(frontend_build, item)
        dst = os.path.join(static_dir, item)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)