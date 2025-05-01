from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ...db.database import get_db
from ...db.crud import get_middleware_projects, get_middleware_project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("")
async def list_projects(db: Session = Depends(get_db)):
    """Get all middleware projects"""
    try:
        projects = get_middleware_projects(db)
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve projects: {str(e)}"
        )

@router.get("/{project_id}")
async def get_project(project_id: str, db: Session = Depends(get_db)):
    """Get middleware project by ID"""
    project = get_middleware_project(project_id, db)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    return project