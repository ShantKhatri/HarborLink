from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import os
import json
import shutil
import zipfile
from typing import Dict, Any, List, Optional

from ...core.api_parser.parser import APIParser
from ...core.api_parser.analyzer import APIAnalyzer
from ...core.transformation.engine import TransformationEngine
from ...core.middleware.generator import MiddlewareGenerator
from ...db.crud import create_middleware_project, get_middleware_project

router = APIRouter(prefix="/middleware", tags=["middleware"])

@router.post("/generate")
async def generate_middleware(
    background_tasks: BackgroundTasks,
    api_spec: UploadFile = File(...),
    framework: str = Form("fastapi"),
    target_standard: str = Form("ondc")
):
    """Generate middleware from API specification"""
    # Create temp file to store uploaded API spec
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(api_spec.file, tmp)
    
    try:
        parser = APIParser()
        api_specification = parser.parse_openapi_spec(tmp_path)
        
        analyzer = APIAnalyzer()
        analysis = analyzer.analyze_api(api_specification)
        
        transformation_engine = TransformationEngine()
        transformation_rules = await transformation_engine.generate_transformations(
            api_specification, target_standard
        )

        middleware_generator = MiddlewareGenerator()
        generated_code = middleware_generator.generate_middleware(
            transformation_rules, framework
        )

        project_id = create_middleware_project({
            "api_name": api_specification.title,
            "framework": framework,
            "target_standard": target_standard,
            "analysis": analysis,
            "generated_code": generated_code
        })

        background_tasks.add_task(os.unlink, tmp_path)
        
        return {
            "project_id": project_id,
            "message": "Middleware generated successfully",
            "api_name": api_specification.title,
            "endpoint_count": len(api_specification.endpoints),
            "framework": framework,
            "target_standard": target_standard
        }
    
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate middleware: {str(e)}"
        )

@router.get("/download/{project_id}")
async def download_middleware(project_id: str):
    """Download generated middleware as zip file"""
    project = get_middleware_project(project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with ID {project_id} not found"
        )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        for filename, code in project["generated_code"].items():
            file_path = os.path.join(tmp_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(code)
        
        zip_path = os.path.join(tmp_dir, f"{project_id}.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    if file == f"{project_id}.zip":
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zipf.write(file_path, arcname)
        
        return FileResponse(
            zip_path, 
            media_type="application/zip",
            filename=f"harborlink-{project_id}.zip"
        )