from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any

from ...core.transformation.engine import TransformationEngine

router = APIRouter(prefix="/transformation", tags=["transformation"])

@router.post("/generate")
async def generate_transformation(
    source_schema: Dict[str, Any] = Body(...),
    target_schema: Dict[str, Any] = Body(...),
    context: Dict[str, Any] = Body({})
):
    """Generate transformation between source and target schemas"""
    try:
        engine = TransformationEngine()
        
        result = await engine.llm_client.generate_transformation(
            source_schema, 
            target_schema, 
            context
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate transformation: {str(e)}"
        )