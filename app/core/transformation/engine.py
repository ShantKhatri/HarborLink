from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from ..api_parser.parser import APISpecification, APIEndpoint
from .llm_client import LLMClient

class TransformationRule(BaseModel):
    source_endpoint: str
    source_method: str
    target_endpoint: str
    target_method: str
    request_mapping: Dict[str, Any] = Field(default_factory=dict)
    response_mapping: Dict[str, Any] = Field(default_factory=dict)
    transformation_code: Optional[str] = None

class TransformationEngine:
    def __init__(self):
        self.llm_client = LLMClient()
        
        # Load ONDC/OCEN schema references - in real app, load from actual schema files
        self.ondc_schema = self._load_reference_schema("ondc")
        self.ocen_schema = self._load_reference_schema("ocen")
    
    async def generate_transformations(self, 
                                     api_spec: APISpecification, 
                                     target_standard: str = "ondc") -> List[TransformationRule]:
        """Generate transformation rules for all endpoints in the API specification"""
        transformations = []
        
        target_schema = self.ondc_schema if target_standard.lower() == "ondc" else self.ocen_schema
        
        for endpoint in api_spec.endpoints:
            target_endpoint = self._find_matching_endpoint(endpoint, target_schema, target_standard)
            
            if target_endpoint:
                request_transformation = await self._generate_request_transformation(endpoint, target_endpoint)
                
                response_transformation = await self._generate_response_transformation(endpoint, target_endpoint)
                
                transformations.append(TransformationRule(
                    source_endpoint=endpoint.path,
                    source_method=endpoint.method,
                    target_endpoint=target_endpoint.get("path", "/unknown"),
                    target_method=target_endpoint.get("method", "get"),
                    request_mapping=request_transformation,
                    response_mapping=response_transformation
                ))
        
        return transformations
    
    def _load_reference_schema(self, schema_type: str) -> Dict[str, Any]:
        """Load reference schema for ONDC or OCEN"""
        # In a real implementation, load from actual schema files
        # For MVP, return simplified placeholder schemas
        if schema_type == "ondc":
            return {
                "endpoints": [
                    {
                        "path": "/search",
                        "method": "post",
                        "request_schema": {"context": {"domain": "string"}, "message": {"intent": {}}},
                        "response_schema": {"context": {}, "message": {"catalog": {}}}
                    },
                    {
                        "path": "/select",
                        "method": "post",
                        "request_schema": {"context": {}, "message": {"order": {}}},
                        "response_schema": {"context": {}, "message": {"order": {}}}
                    }
                ]
            }
        else:
            return {
                "endpoints": [
                    {
                        "path": "/loan/application",
                        "method": "post",
                        "request_schema": {"applicant": {}, "loan": {"amount": "number"}},
                        "response_schema": {"application_id": "string", "status": "string"}
                    }
                ]
            }
    
    def _find_matching_endpoint(self, 
                              source_endpoint: APIEndpoint, 
                              target_schema: Dict[str, Any],
                              target_standard: str) -> Optional[Dict[str, Any]]:
        """Find matching endpoint in target schema"""
        # In a real implementation, use more sophisticated matching logic
        # For MVP, use simplified matching based on endpoint description or path keywords
        
        # Example simplified logic
        path_keywords = source_endpoint.path.lower().split("/")
        method = source_endpoint.method.lower()
        
        for target_endpoint in target_schema.get("endpoints", []):
            target_path = target_endpoint.get("path", "").lower()
            target_method = target_endpoint.get("method", "").lower()
            
            # Simple keyword matching
            for keyword in path_keywords:
                if keyword and keyword in target_path:
                    return target_endpoint
        
        # Return default endpoint if no match found
        return target_schema.get("endpoints", [{}])[0] if target_schema.get("endpoints") else None
    
    async def _generate_request_transformation(self, 
                                            source_endpoint: APIEndpoint, 
                                            target_endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate transformation for request payload"""
        source_schema = source_endpoint.request_body.get("content", {}).get("application/json", {}).get("schema", {}) if source_endpoint.request_body else {}
        target_schema = target_endpoint.get("request_schema", {})
        
        context = {
            "source_endpoint": source_endpoint.path,
            "source_method": source_endpoint.method,
            "target_endpoint": target_endpoint.get("path"),
            "target_method": target_endpoint.get("method")
        }
        
        result = await self.llm_client.generate_transformation(source_schema, target_schema, context)
        return result.get("mapping", {})
    
    async def _generate_response_transformation(self, 
                                             source_endpoint: APIEndpoint, 
                                             target_endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate transformation for response payload"""
        # Get 200 OK response schema from source endpoint
        source_schema = (source_endpoint.responses.get("200", {})
                         .get("content", {})
                         .get("application/json", {})
                         .get("schema", {}))
        
        target_schema = target_endpoint.get("response_schema", {})
        
        context = {
            "source_endpoint": source_endpoint.path,
            "source_method": source_endpoint.method,
            "target_endpoint": target_endpoint.get("path"),
            "target_method": target_endpoint.get("method"),
            "is_response": True
        }
        
        result = await self.llm_client.generate_transformation(target_schema, source_schema, context)
        return result.get("mapping", {})