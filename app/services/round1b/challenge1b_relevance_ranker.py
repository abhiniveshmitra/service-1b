"""
Updated Round 1B Relevance Ranker for Challenge 1B Compliance
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

from config.settings import Settings  # ADD THIS IMPORT
from services.round1b.document_loader import DocumentLoader
from services.round1b.persona_matcher import PersonaMatcher
from services.round1b.challenge1b_input_handler import Challenge1BInputHandler
from services.round1b.challenge1b_output_formatter import Challenge1BOutputFormatter
from utils.file_handler import FileHandler
from utils.logger import setup_logger

class Challenge1BRelevanceRanker:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.settings = Settings()  # ADD THIS
        self.document_loader = DocumentLoader()
        self.persona_matcher = PersonaMatcher()
        self.file_handler = FileHandler()
        self.input_handler = Challenge1BInputHandler()
        self.output_formatter = Challenge1BOutputFormatter()
    
    def process(self):
        """Main processing pipeline for Challenge 1B"""
        # ✅ FIXED - Use collections directory for Service 1B
        collections_dir = self.settings.get_collections_path()
        
        self.logger.info(f"Processing collections from: {collections_dir.absolute()}")
        
        if not collections_dir.exists():
            self.logger.error("Collections directory not found")
            return
        
        # Process each collection directory
        collection_dirs = [d for d in collections_dir.iterdir() if d.is_dir()]
        
        if not collection_dirs:
            self.logger.warning("No collection directories found")
            return
        
        self.logger.info(f"Found {len(collection_dirs)} collections to process")
        
        for collection_dir in collection_dirs:
            try:
                self.logger.info(f'Processing collection: {collection_dir.name}')
                
                # Look for challenge1b_input.json in collection directory
                challenge_input_file = collection_dir / self.settings.challenge_input_file
                
                if not challenge_input_file.exists():
                    self.logger.warning(f'No {self.settings.challenge_input_file} found in {collection_dir.name}')
                    continue
                
                # Load and convert challenge input
                challenge_input = self.input_handler.load_challenge_input(challenge_input_file)
                query_data = self.input_handler.convert_to_internal_format(challenge_input)
                
                # Process the challenge
                result = self.rank_for_challenge(query_data, collection_dir)
                
                # Save result in same collection directory
                output_file = collection_dir / self.settings.challenge_output_file
                
                # Save result
                if self.file_handler.save_json(result, output_file):
                    self.logger.info(f'✅ Completed collection {collection_dir.name}')
                    self.logger.info(f'   Output saved: {output_file.name}')
                else:
                    self.logger.error(f'❌ Failed to save output for {collection_dir.name}')
                
            except Exception as e:
                self.logger.error(f'❌ Error processing collection {collection_dir.name}: {str(e)}')
                import traceback
                self.logger.error(traceback.format_exc())
    
    def rank_for_challenge(self, query_data: Dict, collection_dir: Path) -> Dict:
        """Process single challenge with persona-driven ranking"""
        job_role = query_data.get('job_role', '')
        search_query = query_data.get('query', '')
        documents = query_data.get('documents', [])
        
        all_sections = []
        all_ranked_sections = []
        
        for doc_info in documents:
            # ✅ FIXED - Look for outline file in same collection directory
            outline_path = collection_dir / doc_info['outline_file']
            
            self.logger.debug(f'Looking for outline: {outline_path}')
            
            if outline_path.exists():
                try:
                    # Load document outline
                    outline_data = self.file_handler.load_json(outline_path)
                    sections = outline_data.get('outline', [])
                    
                    # Add document name to each section
                    for section in sections:
                        section['document'] = doc_info['name']
                    
                    all_sections.extend(sections)
                    
                    # Rank sections for this document
                    ranked_sections = self.persona_matcher.rank_sections(
                        sections, job_role, search_query
                    )
                    
                    all_ranked_sections.extend(ranked_sections)
                    
                    self.logger.info(f'   Processed {len(sections)} sections from {doc_info["name"]}')
                    
                except Exception as e:
                    self.logger.error(f'Error processing {doc_info["name"]}: {str(e)}')
            else:
                self.logger.warning(f'Outline not found: {outline_path}')
        
        # Sort all sections by relevance score
        all_ranked_sections.sort(key=lambda x: x[1], reverse=True)
        
        self.logger.info(f'   Total ranked sections: {len(all_ranked_sections)}')
        
        # Format to challenge1b output structure
        return self.output_formatter.format_challenge_output(
            query_data, all_ranked_sections, all_sections
        )
    
    def process_single_collection(self, collection_path: Path) -> bool:
        """Process a single collection - helper method"""
        try:
            challenge_input_file = collection_path / self.settings.challenge_input_file
            
            if not challenge_input_file.exists():
                return False
            
            challenge_input = self.input_handler.load_challenge_input(challenge_input_file)
            query_data = self.input_handler.convert_to_internal_format(challenge_input)
            result = self.rank_for_challenge(query_data, collection_path)
            
            output_file = collection_path / self.settings.challenge_output_file
            return self.file_handler.save_json(result, output_file)
            
        except Exception as e:
            self.logger.error(f'Error processing collection {collection_path.name}: {str(e)}')
            return False
