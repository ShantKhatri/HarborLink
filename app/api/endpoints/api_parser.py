from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import json
import shutil
from typing import Dict, Any

from ...core.api_parser.parser import APIParser
from ...core.api_parser.analyzer import APIAnalyzer

router = APIRouter(prefix="/parser", tags=["parser"])

@router.post("/analyze")
async def analyze_api(
    api_spec: UploadFile = File(...),
):
    """Analyze an API specification"""
    # Create temp file to store uploaded API spec
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(api_spec.file, tmp)
    
    try:
        parser = APIParser()
        api_specification = parser.parse_openapi_spec(tmp_path)
        
        analyzer = APIAnalyzer()
        analysis = analyzer.analyze_api(api_specification)

        os.unlink(tmp_path)
        
        return {
            "api_name": api_specification.title,
            "version": api_specification.version,
            "endpoint_count": len(api_specification.endpoints),
            "analysis": analysis
        }
    
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze API: {str(e)}"
        )