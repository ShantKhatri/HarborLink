import os
import json
from typing import Dict, Any, List, Optional, Union
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        """Initialize LLM client with API key from environment"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_transformation(self, 
                                source_schema: Dict[str, Any],
                                target_schema: Dict[str, Any],
                                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate transformation mapping between source and target schemas"""
        
        prompt = self._create_transformation_prompt(source_schema, target_schema, context)
        
        try:
            # Using Gemini API
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 2000,
                }
            )
            
            transformation_text = response.text
            
            try:
                transformation_json = json.loads(transformation_text)
                return {"mapping": transformation_json}
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', transformation_text, re.DOTALL)
                if json_match:
                    try:
                        transformation_json = json.loads(json_match.group(1))
                        return {"mapping": transformation_json}
                    except:
                        pass
                return {"mapping": {}, "error": "Invalid JSON response"}
        
        except Exception as e:
            return {
                "error": str(e),
                "mapping": {}
            }
    
    def _create_transformation_prompt(self, 
                                     source_schema: Dict[str, Any],
                                     target_schema: Dict[str, Any],
                                     context: Optional[Dict[str, Any]] = None) -> str:
        """Create prompt for the LLM to generate transformation logic"""
        
        prompt = f"""
        I need to transform data from a source API schema to a target API schema.
        
        SOURCE SCHEMA:
        ```json
        {source_schema}
        ```
        
        TARGET SCHEMA (ONDC/OCEN format):
        ```json
        {target_schema}
        ```
        
        Please provide a detailed mapping between these schemas in JSON format, including:
        1. Field mappings (source field -> target field)
        2. Any data transformations needed (type conversions, format changes, etc.)
        3. Default values for any required target fields not in the source
        4. How to handle lists/arrays in either schema
        
        Return ONLY valid JSON that specifies the complete mapping.
        """
        
        if context:
            prompt += f"\n\nAdditional context:\n{context}\n"
            
        return prompt