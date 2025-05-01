import json
import os
from typing import Dict, Any, List, Optional, Tuple, Union
from jsonschema import Draft7Validator, ValidationError
from pydantic import BaseModel, Field

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[Dict[str, Any]] = Field(default_factory=list)
    schema_id: str

class SchemaValidator:
    def __init__(self):
        """Initialize validator with schema references"""
        self.schemas = self._load_schemas()
    
    def validate(self, 
                data: Dict[str, Any], 
                schema_id: str) -> ValidationResult:
        """Validate data against specified schema"""
        schema = self.schemas.get(schema_id)
        
        if not schema:
            return ValidationResult(
                is_valid=False,
                errors=[{"message": f"Schema ID '{schema_id}' not found"}],
                schema_id=schema_id
            )
        
        validator = Draft7Validator(schema)
        errors = []
        
        for error in validator.iter_errors(data):
            errors.append({
                "path": "/".join([str(p) for p in error.path]),
                "message": error.message,
                "schema_path": "/".join([str(p) for p in error.schema_path])
            })
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            schema_id=schema_id
        )
    
    def generate_report(self, validation_result: ValidationResult) -> Dict[str, Any]:
        """Generate a validation report with details and suggestions"""
        report = {
            "is_valid": validation_result.is_valid,
            "schema_id": validation_result.schema_id,
            "error_count": len(validation_result.errors),
            "warning_count": len(validation_result.warnings),
            "detailed_errors": validation_result.errors,
            "detailed_warnings": validation_result.warnings,
            "suggestions": self._generate_suggestions(validation_result)
        }
        
        return report
    
    def _load_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Load JSON schemas for ONDC and OCEN"""
        schemas_dir = os.path.join(os.path.dirname(__file__), 'schemas')
        schemas = {}
        
        # Load ONDC schemas
        ondc_dir = os.path.join(schemas_dir, 'ondc')
        if os.path.exists(ondc_dir):
            for filename in os.listdir(ondc_dir):
                if filename.endswith('.json'):
                    schema_path = os.path.join(ondc_dir, filename)
                    schema_id = f"ondc/{filename[:-5]}"  # Remove .json extension
                    with open(schema_path, 'r') as f:
                        schemas[schema_id] = json.load(f)
        
        # Load OCEN schemas
        ocen_dir = os.path.join(schemas_dir, 'ocen')
        if os.path.exists(ocen_dir):
            for filename in os.listdir(ocen_dir):
                if filename.endswith('.json'):
                    schema_path = os.path.join(ocen_dir, filename)
                    schema_id = f"ocen/{filename[:-5]}"  # Remove .json extension
                    with open(schema_path, 'r') as f:
                        schemas[schema_id] = json.load(f)
        
        if not schemas:
            schemas = {
                "ondc/search": {
                    "type": "object",
                    "required": ["context", "message"],
                    "properties": {
                        "context": {
                            "type": "object", 
                            "required": ["domain"]
                        },
                        "message": {"type": "object"}
                    }
                },
                "ocen/loan_application": {
                    "type": "object",
                    "required": ["applicant", "loan"],
                    "properties": {
                        "applicant": {"type": "object"},
                        "loan": {
                            "type": "object",
                            "required": ["amount"]
                        }
                    }
                }
            }
        
        return schemas
    
    def _generate_suggestions(self, validation_result: ValidationResult) -> List[str]:
        """Generate suggestions to fix validation issues"""
        suggestions = []
        
        for error in validation_result.errors:
            path = error.get("path", "")
            message = error.get("message", "")
            
            if "required property" in message:
                missing_prop = message.split("'")[-2]
                suggestions.append(f"Add the required property '{missing_prop}' at path '{path}'")
            
            elif "is not of type" in message:
                wrong_type = message.split("is not of type ")[-1]
                suggestions.append(f"Fix type at path '{path}' - expected {wrong_type}")
        
        return suggestions