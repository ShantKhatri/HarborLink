import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from . import models, database

def create_middleware_project(project_data: Dict[str, Any], db: Session = None) -> str:
    """Create a new middleware project in the database"""
    if db is None:
        db = next(database.get_db())
    
    project_id = str(uuid.uuid4())
    
    # Create project
    project = models.Project(
        id=project_id,
        api_name=project_data["api_name"],
        framework=project_data["framework"],
        target_standard=project_data["target_standard"]
    )
    
    db.add(project)
    
    # Create transformations
    if "generated_code" in project_data:
        for filename, code in project_data["generated_code"].items():
            # Only store core files in the transformation table
            if filename in ["app.js", "main.py", "router.py", "router.js"]:
                transformation = models.Transformation(
                    project_id=project_id,
                    source_endpoint="/",  # Placeholder
                    source_method="get",  # Placeholder
                    target_endpoint="/",  # Placeholder
                    target_method="get",  # Placeholder
                    transformation_code=code
                )
                db.add(transformation)
    
    db.commit()
    return project_id

def get_middleware_project(project_id: str, db: Session = None) -> Optional[Dict[str, Any]]:
    """Get middleware project by ID"""
    if db is None:
        db = next(database.get_db())
    
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    
    if not project:
        return None
    
    transformations = db.query(models.Transformation).filter(
        models.Transformation.project_id == project_id
    ).all()
    
    project_dict = {
        "id": project.id,
        "api_name": project.api_name,
        "framework": project.framework,
        "target_standard": project.target_standard,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "generated_code": {}
    }
    
    for transformation in transformations:
        if transformation.transformation_code:
            if transformation.source_endpoint != "/":
                filename = f"endpoint_{transformation.source_endpoint.replace('/', '_')}.py"
            else:
                if project.framework.lower() == "fastapi":
                    filename = "main.py"
                else:
                    filename = "app.js"
            
            project_dict["generated_code"][filename] = transformation.transformation_code
    
    return project_dict

def get_middleware_projects(db: Session = None) -> List[Dict[str, Any]]:
    """Get all middleware projects"""
    if db is None:
        db = next(database.get_db())
    
    projects = db.query(models.Project).order_by(models.Project.created_at.desc()).all()
    
    return [
        {
            "id": project.id,
            "api_name": project.api_name,
            "framework": project.framework,
            "target_standard": project.target_standard,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        for project in projects
    ]