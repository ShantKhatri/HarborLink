import json
import yaml
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class APIEndpoint(BaseModel):
    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: List[Dict[str, Any]] = Field(default_factory=list)
    request_body: Optional[Dict[str, Any]] = None
    responses: Dict[str, Any] = Field(default_factory=dict)
    security: List[Dict[str, List[str]]] = Field(default_factory=list)

class APISpecification(BaseModel):
    title: str
    version: str
    description: Optional[str] = None
    endpoints: List[APIEndpoint] = Field(default_factory=list)
    security_schemes: Dict[str, Any] = Field(default_factory=dict)

class APIParser:
    def parse_openapi_spec(self, spec_path: str) -> APISpecification:
        """Parse OpenAPI 3.0 specification file"""
        with open(spec_path, 'r') as f:
            if spec_path.endswith('.json'):
                spec = json.load(f)
            elif spec_path.endswith(('.yaml', '.yml')):
                spec = yaml.safe_load(f)
            else:
                raise ValueError("Unsupported file format. Only JSON and YAML are supported.")
        
        return self._process_spec(spec)
    
    def _process_spec(self, spec: Dict[str, Any]) -> APISpecification:
        """Process the OpenAPI spec into our internal format"""
        endpoints = []
        
        for path, path_item in spec.get('paths', {}).items():
            for method, operation in path_item.items():
                if method in ['get', 'post', 'put', 'delete', 'patch']:
                    endpoints.append(APIEndpoint(
                        path=path,
                        method=method,
                        summary=operation.get('summary'),
                        description=operation.get('description'),
                        parameters=operation.get('parameters', []),
                        request_body=operation.get('requestBody'),
                        responses=operation.get('responses', {}),
                        security=operation.get('security', [])
                    ))
        
        security_schemes = spec.get('components', {}).get('securitySchemes', {})
        
        return APISpecification(
            title=spec.get('info', {}).get('title', 'Unknown API'),
            version=spec.get('info', {}).get('version', '0.0.0'),
            description=spec.get('info', {}).get('description'),
            endpoints=endpoints,
            security_schemes=security_schemes
        )