import os
import json
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader
from ..transformation.engine import TransformationRule

class MiddlewareGenerator:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
    def generate_middleware(self, 
                           transformation_rules: List[TransformationRule], 
                           framework: str = "fastapi") -> Dict[str, str]:
        """Generate middleware code based on transformation rules"""
        if framework.lower() == "fastapi":
            return self._generate_fastapi_middleware(transformation_rules)
        elif framework.lower() == "express":
            return self._generate_express_middleware(transformation_rules)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
    
    def _generate_fastapi_middleware(self, transformation_rules: List[TransformationRule]) -> Dict[str, str]:
        """Generate FastAPI middleware code"""
        main_template = self.env.get_template('fastapi/main.py.j2')
        router_template = self.env.get_template('fastapi/router.py.j2')
        endpoint_template = self.env.get_template('fastapi/endpoint.py.j2')
        
        main_code = main_template.render(
            project_name="HarborLink Middleware",
            description="API middleware for ONDC/OCEN compliance",
            version="0.1.0"
        )
        
        router_code = router_template.render(
            transformation_rules=transformation_rules
        )
        
        endpoint_files = {}
        for i, rule in enumerate(transformation_rules):
            endpoint_code = endpoint_template.render(
                rule=rule,
                endpoint_id=f"endpoint_{i + 1}"
            )
            endpoint_files[f"endpoint_{rule.source_endpoint.replace('/', '_')}.py"] = endpoint_code
        
        generated_code = {
            "main.py": main_code,
            "router.py": router_code,
            **endpoint_files
        }
        
        return generated_code
    
    def _generate_express_middleware(self, transformation_rules: List[TransformationRule]) -> Dict[str, str]:
        """Generate Express.js middleware code"""
        app_template = self.env.get_template('express/app.js.j2')
        router_template = self.env.get_template('express/router.js.j2')
        endpoint_template = self.env.get_template('express/endpoint.js.j2')
        
        app_code = app_template.render(
            project_name="HarborLink Middleware",
            description="API middleware for ONDC/OCEN compliance"
        )
        
        router_code = router_template.render(
            transformation_rules=transformation_rules
        )
        
        endpoint_files = {}
        for i, rule in enumerate(transformation_rules):
            endpoint_code = endpoint_template.render(
                rule=rule,
                endpoint_id=f"endpoint_{i + 1}"
            )
            endpoint_files[f"endpoint_{rule.source_endpoint.replace('/', '_')}.js"] = endpoint_code
        
        generated_code = {
            "app.js": app_code,
            "router.js": router_code,
            **endpoint_files
        }
        
        return generated_code