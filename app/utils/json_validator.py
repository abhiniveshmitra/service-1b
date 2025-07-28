"""
JSON validation utilities for Service 1B - Challenge 1B Format Compliance
"""

import json
import logging
from typing import Dict, List, Union
from pathlib import Path

class JSONValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_challenge1b_input(self, input_data: Dict) -> tuple[bool, List[str]]:
        """Validate challenge1b_input.json format"""
        errors = []
        
        # Check required top-level fields for Challenge 1B input
        required_fields = ['challenge_info', 'documents', 'persona', 'job_to_be_done']
        for field in required_fields:
            if field not in input_data:
                errors.append(f'Missing required field: {field}')
        
        # Validate challenge_info structure
        if 'challenge_info' in input_data:
            challenge_info = input_data['challenge_info']
            if not isinstance(challenge_info, dict):
                errors.append('challenge_info must be an object')
            else:
                if 'challenge_id' not in challenge_info:
                    errors.append('challenge_info missing challenge_id')
        
        # Validate documents structure
        if 'documents' in input_data:
            documents = input_data['documents']
            if not isinstance(documents, list):
                errors.append('documents must be an array')
            else:
                for idx, doc in enumerate(documents):
                    if not isinstance(doc, dict):
                        errors.append(f'Document {idx} must be an object')
                        continue
                    if 'filename' not in doc:
                        errors.append(f'Document {idx} missing filename')
        
        # Validate persona structure
        if 'persona' in input_data:
            persona = input_data['persona']
            if not isinstance(persona, dict):
                errors.append('persona must be an object')
            elif 'role' not in persona:
                errors.append('persona missing role field')
        
        # Validate job_to_be_done structure
        if 'job_to_be_done' in input_data:
            job = input_data['job_to_be_done']
            if not isinstance(job, dict):
                errors.append('job_to_be_done must be an object')
            elif 'task' not in job:
                errors.append('job_to_be_done missing task field')
        
        return len(errors) == 0, errors
    
    def validate_challenge1b_output(self, output_data: Dict) -> tuple[bool, List[str]]:
        """Validate challenge1b_output.json format"""
        errors = []
        
        # Check required top-level fields for Challenge 1B output
        required_fields = ['metadata', 'extracted_sections', 'subsection_analysis']
        for field in required_fields:
            if field not in output_data:
                errors.append(f'Missing required field: {field}')
        
        # Validate metadata structure
        if 'metadata' in output_data:
            metadata = output_data['metadata']
            if not isinstance(metadata, dict):
                errors.append('metadata must be an object')
            else:
                metadata_fields = ['input_documents', 'persona', 'job_to_be_done']
                for field in metadata_fields:
                    if field not in metadata:
                        errors.append(f'metadata missing field: {field}')
        
        # Validate extracted_sections structure
        if 'extracted_sections' in output_data:
            extracted_sections = output_data['extracted_sections']
            if not isinstance(extracted_sections, list):
                errors.append('extracted_sections must be an array')
            else:
                for idx, section in enumerate(extracted_sections):
                    section_errors = self._validate_extracted_section(section, idx)
                    errors.extend(section_errors)
        
        # Validate subsection_analysis structure
        if 'subsection_analysis' in output_data:
            subsection_analysis = output_data['subsection_analysis']
            if not isinstance(subsection_analysis, list):
                errors.append('subsection_analysis must be an array')
            else:
                for idx, subsection in enumerate(subsection_analysis):
                    subsection_errors = self._validate_subsection_analysis(subsection, idx)
                    errors.extend(subsection_errors)
        
        return len(errors) == 0, errors
    
    def _validate_extracted_section(self, section: Dict, idx: int) -> List[str]:
        """Validate individual extracted section"""
        errors = []
        
        required_fields = ['document', 'section_title', 'importance_rank', 'page_number']
        for field in required_fields:
            if field not in section:
                errors.append(f'Extracted section {idx} missing field: {field}')
        
        # Validate field types
        if 'importance_rank' in section:
            if not isinstance(section['importance_rank'], int) or section['importance_rank'] < 1:
                errors.append(f'Extracted section {idx} importance_rank must be positive integer')
        
        if 'page_number' in section:
            if not isinstance(section['page_number'], int) or section['page_number'] < 1:
                errors.append(f'Extracted section {idx} page_number must be positive integer')
        
        return errors
    
    def _validate_subsection_analysis(self, subsection: Dict, idx: int) -> List[str]:
        """Validate individual subsection analysis"""
        errors = []
        
        required_fields = ['document', 'refined_text', 'page_number']
        for field in required_fields:
            if field not in subsection:
                errors.append(f'Subsection analysis {idx} missing field: {field}')
        
        # Validate field types
        if 'refined_text' in subsection:
            if not isinstance(subsection['refined_text'], str) or not subsection['refined_text'].strip():
                errors.append(f'Subsection analysis {idx} refined_text must be non-empty string')
        
        if 'page_number' in subsection:
            if not isinstance(subsection['page_number'], int) or subsection['page_number'] < 1:
                errors.append(f'Subsection analysis {idx} page_number must be positive integer')
        
        return errors
    
    def validate_input_file(self, file_path: Union[str, Path]) -> tuple[bool, List[str]]:
        """Validate challenge1b_input.json file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return False, [f'File does not exist: {file_path}']
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self.validate_challenge1b_input(data)
                
        except json.JSONDecodeError as e:
            return False, [f'Invalid JSON format: {str(e)}']
        except Exception as e:
            return False, [f'Error reading file: {str(e)}']
    
    def validate_output_file(self, file_path: Union[str, Path]) -> tuple[bool, List[str]]:
        """Validate challenge1b_output.json file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return False, [f'File does not exist: {file_path}']
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self.validate_challenge1b_output(data)
                
        except json.JSONDecodeError as e:
            return False, [f'Invalid JSON format: {str(e)}']
        except Exception as e:
            return False, [f'Error reading file: {str(e)}']
    
    def validate_collection_files(self, collection_dir: Union[str, Path]) -> Dict[str, tuple[bool, List[str]]]:
        """Validate all JSON files in a collection directory"""
        results = {}
        collection_dir = Path(collection_dir)
        
        if not collection_dir.exists():
            return {'error': (False, [f'Collection directory does not exist: {collection_dir}'])}
        
        # Check for input file
        input_file = collection_dir / 'challenge1b_input.json'
        if input_file.exists():
            results['input'] = self.validate_input_file(input_file)
        else:
            results['input'] = (False, ['challenge1b_input.json not found'])
        
        # Check for output file
        output_file = collection_dir / 'challenge1b_output.json'
        if output_file.exists():
            results['output'] = self.validate_output_file(output_file)
        else:
            results['output'] = (True, ['challenge1b_output.json not found (will be generated)'])
        
        return results
    
    def get_expected_input_schema(self) -> Dict:
        """Return expected JSON schema for challenge1b_input.json"""
        return {
            "type": "object",
            "required": ["challenge_info", "documents", "persona", "job_to_be_done"],
            "properties": {
                "challenge_info": {
                    "type": "object",
                    "required": ["challenge_id"],
                    "properties": {
                        "challenge_id": {"type": "string"},
                        "test_case_name": {"type": "string"}
                    }
                },
                "documents": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["filename"],
                        "properties": {
                            "filename": {"type": "string"},
                            "title": {"type": "string"}
                        }
                    }
                },
                "persona": {
                    "type": "object",
                    "required": ["role"],
                    "properties": {
                        "role": {"type": "string"}
                    }
                },
                "job_to_be_done": {
                    "type": "object",
                    "required": ["task"],
                    "properties": {
                        "task": {"type": "string"}
                    }
                }
            }
        }
    
    def get_expected_output_schema(self) -> Dict:
        """Return expected JSON schema for challenge1b_output.json"""
        return {
            "type": "object",
            "required": ["metadata", "extracted_sections", "subsection_analysis"],
            "properties": {
                "metadata": {
                    "type": "object",
                    "required": ["input_documents", "persona", "job_to_be_done"],
                    "properties": {
                        "input_documents": {"type": "array", "items": {"type": "string"}},
                        "persona": {"type": "string"},
                        "job_to_be_done": {"type": "string"}
                    }
                },
                "extracted_sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["document", "section_title", "importance_rank", "page_number"],
                        "properties": {
                            "document": {"type": "string"},
                            "section_title": {"type": "string"},
                            "importance_rank": {"type": "integer", "minimum": 1},
                            "page_number": {"type": "integer", "minimum": 1}
                        }
                    }
                },
                "subsection_analysis": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["document", "refined_text", "page_number"],
                        "properties": {
                            "document": {"type": "string"},
                            "refined_text": {"type": "string"},
                            "page_number": {"type": "integer", "minimum": 1}
                        }
                    }
                }
            }
        }
