"""
Updated Adobe Hackathon Challenge 1B Input Handler
Handles exact official specification format
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

class Challenge1BInputHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_challenge_input(self, input_file: Path) -> Dict:
        """Load challenge1b_input.json with exact specification format"""
        try:
            with open(input_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            # Validate required fields
            required_fields = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            self.logger.info(f"Loaded challenge input with {len(data.get('documents', []))} documents")
            return data
            
        except Exception as e:
            self.logger.error(f'Error loading challenge input from {input_file}: {str(e)}')
            raise
    
    def convert_to_internal_format(self, challenge_input: Dict) -> Dict:
        """Convert official challenge input to internal query format"""
        
        # Extract challenge info
        challenge_info = challenge_input.get("challenge_info", {})
        challenge_id = challenge_info.get("challenge_id", "")
        test_case_name = challenge_info.get("test_case_name", "")
        
        # Extract persona and job information  
        persona = challenge_input.get("persona", {})
        persona_role = persona.get("role", "")
        
        job_to_be_done = challenge_input.get("job_to_be_done", {})
        task = job_to_be_done.get("task", "")
        
        # Convert documents format
        documents = []
        for doc in challenge_input.get("documents", []):
            filename = doc.get("filename", "")
            title = doc.get("title", filename.replace(".pdf", ""))
            
            documents.append({
                "name": filename,
                "title": title,
                "outline_file": filename.replace(".pdf", "_outline.json")
            })
        
        return {
            "challenge_id": challenge_id,
            "test_case_name": test_case_name,
            "job_role": persona_role,
            "query": task,
            "documents": documents,
            "original_input": challenge_input  # Keep for metadata
        }
    
    def validate_input_schema(self, data: Dict) -> bool:
        """Validate input follows official specification"""
        try:
            # Check top-level structure
            required_keys = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
            for key in required_keys:
                if key not in data:
                    self.logger.error(f"Missing required top-level key: {key}")
                    return False
            
            # Validate challenge_info
            challenge_info = data['challenge_info']
            if not isinstance(challenge_info, dict):
                self.logger.error("challenge_info must be an object")
                return False
            
            # Validate documents
            documents = data['documents']
            if not isinstance(documents, list):
                self.logger.error("documents must be an array")
                return False
            
            for doc in documents:
                if 'filename' not in doc:
                    self.logger.error("Each document must have a filename")
                    return False
            
            # Validate persona
            persona = data['persona']
            if not isinstance(persona, dict) or 'role' not in persona:
                self.logger.error("persona must have a role field")
                return False
            
            # Validate job_to_be_done
            job = data['job_to_be_done']
            if not isinstance(job, dict) or 'task' not in job:
                self.logger.error("job_to_be_done must have a task field")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating schema: {str(e)}")
            return False
