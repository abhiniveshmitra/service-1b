"""
Document loading and preprocessing for Round 1B
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from utils.file_handler import FileHandler

class DocumentLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_handler = FileHandler()
    
    def load_outline(self, outline_path: str) -> Optional[Dict]:
        """Load and validate document outline from Round 1A"""
        try:
            outline_data = self.file_handler.load_json(outline_path)
            
            # Validate structure
            if not self._validate_outline_structure(outline_data):
                self.logger.warning(f'Invalid outline structure in {outline_path}')
                return None
            
            return outline_data
            
        except Exception as e:
            self.logger.error(f'Error loading outline {outline_path}: {str(e)}')
            return None
    
    def _validate_outline_structure(self, outline_data: Dict) -> bool:
        """Validate outline JSON structure"""
        required_fields = ['document', 'outline']
        
        for field in required_fields:
            if field not in outline_data:
                return False
        
        # Validate outline sections
        outline = outline_data['outline']
        if not isinstance(outline, list):
            return False
        
        return True
    
    def extract_searchable_content(self, outline_data: Dict) -> List[Dict]:
        """Extract all searchable content sections from outline"""
        sections = []
        
        def extract_recursive(items: List[Dict], parent_context: str = ''):
            for item in items:
                section_text = item.get('text', '')
                full_context = f'{parent_context} {section_text}'.strip()
                
                sections.append({
                    'text': section_text,
                    'full_context': full_context,
                    'level': item.get('level', 1),
                    'confidence': item.get('confidence', 0.0),
                    'page': item.get('page', 0),
                    'has_children': len(item.get('children', [])) > 0
                })
                
                # Recursively process children
                if 'children' in item and item['children']:
                    extract_recursive(item['children'], full_context)
        
        outline = outline_data.get('outline', [])
        extract_recursive(outline)
        
        return sections
    
    def load_multiple_outlines(self, outline_files: List[str]) -> Dict[str, Dict]:
        """Load multiple outline files"""
        loaded_outlines = {}
        
        for file_path in outline_files:
            outline_data = self.load_outline(file_path)
            if outline_data:
                doc_name = outline_data.get('document', Path(file_path).stem)
                loaded_outlines[doc_name] = outline_data
        
        return loaded_outlines
