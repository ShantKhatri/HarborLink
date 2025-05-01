from typing import Dict, Any, List, Set
from .parser import APISpecification, APIEndpoint

class APIAnalyzer:
    def analyze_api(self, api_spec: APISpecification) -> Dict[str, Any]:
        """Analyze API specification and identify key characteristics"""
        analysis = {
            "auth_methods": self._identify_auth_methods(api_spec),
            "data_formats": self._identify_data_formats(api_spec),
            "required_transformations": self._identify_transformations(api_spec),
            "endpoint_summary": self._summarize_endpoints(api_spec)
        }
        return analysis
    
    def _identify_auth_methods(self, api_spec: APISpecification) -> List[str]:
        """Identify authentication methods used in the API"""
        auth_methods = set()
        
        for scheme_name, scheme in api_spec.security_schemes.items():
            auth_type = scheme.get('type')
            if auth_type:
                if auth_type == 'oauth2':
                    auth_methods.add('OAuth2')
                elif auth_type == 'http':
                    scheme_scheme = scheme.get('scheme', '').lower()
                    if scheme_scheme == 'bearer':
                        auth_methods.add('JWT/Bearer Token')
                    elif scheme_scheme == 'basic':
                        auth_methods.add('Basic Auth')
                elif auth_type == 'apiKey':
                    auth_methods.add('API Key')
        
        return list(auth_methods)
    
    def _identify_data_formats(self, api_spec: APISpecification) -> Dict[str, Set[str]]:
        """Identify data formats used in request/response bodies"""
        request_formats = set()
        response_formats = set()
        
        for endpoint in api_spec.endpoints:
            if endpoint.request_body and 'content' in endpoint.request_body:
                for media_type in endpoint.request_body['content'].keys():
                    request_formats.add(media_type)
            
            for response in endpoint.responses.values():
                if 'content' in response:
                    for media_type in response['content'].keys():
                        response_formats.add(media_type)
        
        return {
            "request_formats": list(request_formats),
            "response_formats": list(response_formats)
        }
    
    def _identify_transformations(self, api_spec: APISpecification) -> List[Dict[str, Any]]:
        """Identify required transformations for ONDC/OCEN compliance"""
        # This is a placeholder for MVP
        # In a real implementation, this would compare with ONDC/OCEN specs
        transformations = []
        
        for endpoint in api_spec.endpoints:
            transformations.append({
                "source_path": endpoint.path,
                "source_method": endpoint.method,
                "transformation_type": "structural",  # placeholder
                "complexity": "medium"  # placeholder
            })
        
        return transformations
    
    def _summarize_endpoints(self, api_spec: APISpecification) -> Dict[str, int]:
        """Summarize endpoints by method"""
        summary = {}
        
        for endpoint in api_spec.endpoints:
            method = endpoint.method.upper()
            summary[method] = summary.get(method, 0) + 1
        
        return summary