from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List, Optional

from ...core.validator.schema_validator import SchemaValidator

router = APIRouter(prefix="/validator", tags=["validator"])

@router.post("/validate")
async def validate_api(
    data: Dict[str, Any] = Body(...),
    schema_id: str = Body(...)
):
    """Validate API data against ONDC/OCEN schema"""
    try:
        validator = SchemaValidator()
        
        validation_result = validator.validate(data, schema_id)
        
        report = validator.generate_report(validation_result)
        
        return report
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )

@router.get("/schemas")
async def list_schemas():
    """List available validation schemas"""
    try:
        validator = SchemaValidator()
        return {"schemas": list(validator.schemas.keys())}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list schemas: {str(e)}"
        )