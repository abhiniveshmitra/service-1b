"""
Updated Adobe Hackathon Challenge 1B Output Formatter
Generates exact official specification format
"""

import json
from typing import Dict, List, Tuple
from pathlib import Path

class Challenge1BOutputFormatter:
    def __init__(self):
        pass
    
    def format_challenge_output(self, query_data: Dict, ranked_sections: List[Tuple], 
                              all_sections: List[Dict]) -> Dict:
        """Format results to exact challenge1b_output.json specification"""
        
        # Extract metadata from original input
        original_input = query_data.get("original_input", {})
        documents = query_data.get("documents", [])
        
        # Build metadata section (exact spec compliance)
        metadata = {
            "input_documents": [doc["name"] for doc in documents],
            "persona": query_data.get("job_role", ""),
            "job_to_be_done": query_data.get("query", "")
        }
        
        # Build extracted_sections (top-ranked sections with exact spec format)
        extracted_sections = []
        processed_sections = set()  # Avoid duplicates
        
        for idx, (section, score) in enumerate(ranked_sections[:20]):  # Top 20 sections
            section_text = section.get('text', '').strip()
            document_name = section.get('document', 'unknown.pdf')
            page_number = section.get('page', 1)
            
            # Create unique key to avoid duplicates
            section_key = f"{document_name}-{section_text}-{page_number}"
            
            if section_key not in processed_sections and section_text:
                extracted_sections.append({
                    "document": document_name,
                    "section_title": section_text,
                    "importance_rank": len(extracted_sections) + 1,
                    "page_number": page_number
                })
                processed_sections.add(section_key)
        
        # Build subsection_analysis (detailed content analysis)
        subsection_analysis = []
        processed_subsections = set()
        
        for idx, (section, score) in enumerate(ranked_sections[:15]):  # Top 15 for detailed analysis
            section_text = section.get('text', '').strip()
            document_name = section.get('document', 'unknown.pdf')
            page_number = section.get('page', 1)
            
            # Get refined text (combine section text with children if available)
            refined_text = section_text
            if section.get('children'):
                child_texts = [child.get('text', '').strip() for child in section['children'] if child.get('text', '').strip()]
                if child_texts:
                    refined_text += " " + " ".join(child_texts[:3])  # Limit to first 3 children
            
            # Ensure refined text is meaningful
            refined_text = refined_text.strip()
            if len(refined_text) < 5:  # Skip very short text
                continue
            
            subsection_key = f"{document_name}-{refined_text[:50]}-{page_number}"
            
            if subsection_key not in processed_subsections:
                subsection_analysis.append({
                    "document": document_name,
                    "refined_text": refined_text,
                    "page_number": page_number
                })
                processed_subsections.add(subsection_key)
        
        # Build final output structure (exact specification compliance)
        return {
            "metadata": metadata,
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }
    
    def validate_output_schema(self, output_data: Dict) -> bool:
        """Validate output follows official specification"""
        required_keys = ['metadata', 'extracted_sections', 'subsection_analysis']
        
        for key in required_keys:
            if key not in output_data:
                return False
        
        # Validate metadata structure
        metadata = output_data['metadata']
        metadata_keys = ['input_documents', 'persona', 'job_to_be_done']
        for key in metadata_keys:
            if key not in metadata:
                return False
        
        # Validate extracted_sections structure
        for section in output_data['extracted_sections']:
            section_keys = ['document', 'section_title', 'importance_rank', 'page_number']
            for key in section_keys:
                if key not in section:
                    return False
        
        # Validate subsection_analysis structure
        for subsection in output_data['subsection_analysis']:
            subsection_keys = ['document', 'refined_text', 'page_number']
            for key in subsection_keys:
                if key not in subsection:
                    return False
        
        return True
