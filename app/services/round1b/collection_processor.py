"""
Adobe Hackathon Challenge 1B Collection Processor
Discovers and processes multiple collection folders
"""

import logging
from pathlib import Path
from typing import List, Dict
import json

from config.settings import Settings  # ADD THIS IMPORT
from services.round1b.challenge1b_input_handler import Challenge1BInputHandler
from services.round1b.challenge1b_output_formatter import Challenge1BOutputFormatter
from services.round1b.persona_matcher import PersonaMatcher
from utils.file_handler import FileHandler
from utils.logger import setup_logger

class CollectionProcessor:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.settings = Settings()  # ADD THIS
        self.input_handler = Challenge1BInputHandler()
        self.output_formatter = Challenge1BOutputFormatter()
        self.persona_matcher = PersonaMatcher()
        self.file_handler = FileHandler()
    
    def discover_collections(self, root_path: Path = None) -> List[Path]:
        """Discover all collection folders containing challenge1b_input.json"""
        if root_path is None:
            root_path = self.settings.get_collections_path()  # USE SETTINGS
        
        collections = []
        
        if not root_path.exists():
            self.logger.warning(f"Root path does not exist: {root_path}")
            return collections
        
        # Look for collection directories
        for item in root_path.iterdir():
            if item.is_dir():
                input_file = item / self.settings.challenge_input_file  # USE SETTINGS
                if input_file.exists():
                    collections.append(item)
                    self.logger.info(f"Found collection: {item.name}")
        
        self.logger.info(f"Discovered {len(collections)} collections in {root_path}")
        return collections
    
    def process_all_collections(self, root_path: Path = None):
        """Process all discovered collections"""
        if root_path is None:
            root_path = self.settings.get_collections_path()  # USE SETTINGS
        
        # Validate collections directory exists
        if not self.settings.validate_directories():
            self.logger.error("Failed to create/validate directories")
            return
        
        collections = self.discover_collections(root_path)
        
        if not collections:
            self.logger.warning("No collections found with challenge1b_input.json files")
            self.logger.info(f"Expected structure: collections/Collection_Name/{self.settings.challenge_input_file}")
            return
        
        self.logger.info(f"Processing {len(collections)} collections")
        
        successful_count = 0
        failed_count = 0
        
        for collection_path in collections:
            try:
                if self.process_single_collection(collection_path):
                    successful_count += 1
                    self.logger.info(f"✅ Successfully processed {collection_path.name}")
                else:
                    failed_count += 1
                    self.logger.error(f"❌ Failed to process {collection_path.name}")
                    
            except Exception as e:
                failed_count += 1
                self.logger.error(f"❌ Error processing collection {collection_path.name}: {str(e)}")
                import traceback
                self.logger.error(traceback.format_exc())
        
        # Final summary
        self.logger.info("=" * 50)
        self.logger.info(f"Collection processing completed")
        self.logger.info(f"✅ Successfully processed: {successful_count} collections")
        if failed_count > 0:
            self.logger.warning(f"❌ Failed: {failed_count} collections")
    
    def process_single_collection(self, collection_path: Path) -> bool:
        """Process a single collection folder"""
        try:
            start_time = __import__('time').time()
            self.logger.info(f"Processing collection: {collection_path.name}")
            
            # Load challenge input
            input_file = collection_path / self.settings.challenge_input_file
            
            if not input_file.exists():
                self.logger.error(f"Challenge input file not found: {input_file}")
                return False
            
            challenge_input = self.input_handler.load_challenge_input(input_file)
            
            # Validate input schema
            if not self.input_handler.validate_input_schema(challenge_input):
                self.logger.error(f"Invalid input schema in {collection_path.name}")
                return False
            
            # Convert to internal format
            query_data = self.input_handler.convert_to_internal_format(challenge_input)
            
            # Process documents in this collection
            all_ranked_sections = []
            all_sections = []
            
            documents = query_data.get('documents', [])
            job_role = query_data.get('job_role', '')
            search_query = query_data.get('query', '')
            
            self.logger.info(f"   Processing {len(documents)} documents for persona: {job_role}")
            
            for doc_info in documents:
                # ✅ FIXED - Look for outline files in collection directory only
                outline_filename = doc_info['outline_file']
                outline_path = collection_path / outline_filename
                
                self.logger.debug(f"   Looking for outline: {outline_path}")
                
                if outline_path.exists():
                    try:
                        # Load document outline
                        outline_data = self.file_handler.load_json(outline_path)
                        sections = outline_data.get('outline', [])
                        
                        if not sections:
                            self.logger.warning(f"No sections found in {outline_filename}")
                            continue
                        
                        # Add document metadata to each section
                        for section in sections:
                            section['document'] = doc_info['name']
                            section['title'] = doc_info.get('title', doc_info['name'])
                            section['collection'] = collection_path.name
                        
                        all_sections.extend(sections)
                        
                        # Rank sections for this document
                        ranked_sections = self.persona_matcher.rank_sections(
                            sections, job_role, search_query
                        )
                        
                        all_ranked_sections.extend(ranked_sections)
                        
                        self.logger.info(f"   ✅ Processed {len(sections)} sections from {doc_info['name']}")
                        
                    except Exception as e:
                        self.logger.error(f"   ❌ Error processing document {doc_info['name']}: {str(e)}")
                        continue
                else:
                    self.logger.warning(f"   ⚠️  Outline not found: {outline_filename}")
                    continue
            
            if not all_ranked_sections:
                self.logger.warning(f"No sections found to rank in collection {collection_path.name}")
                return False
            
            # Sort all sections by relevance score
            all_ranked_sections.sort(key=lambda x: x[1], reverse=True)
            
            # Format to challenge1b output structure
            result = self.output_formatter.format_challenge_output(
                query_data, all_ranked_sections, all_sections
            )
            
            # Validate output schema
            if not self.output_formatter.validate_output_schema(result):
                self.logger.error(f"Generated output failed schema validation for {collection_path.name}")
                return False
            
            # Save output to collection folder
            output_file = collection_path / self.settings.challenge_output_file
            
            if not self.file_handler.save_json(result, output_file):
                self.logger.error(f"Failed to save output file: {output_file}")
                return False
            
            processing_time = __import__('time').time() - start_time
            challenge_id = query_data.get('challenge_id', 'unknown')
            
            # Check timing compliance (≤60 seconds requirement)
            if processing_time > self.settings.timeout_seconds:
                self.logger.warning(f"Processing time {processing_time:.2f}s exceeds {self.settings.timeout_seconds}s limit")
            
            self.logger.info(f"   📊 Generated {len(result.get('extracted_sections', []))} extracted sections")
            self.logger.info(f"   📊 Generated {len(result.get('subsection_analysis', []))} subsection analyses")
            self.logger.info(f"   ⏱️  Processing time: {processing_time:.2f}s")
            self.logger.info(f"   💾 Output saved: {self.settings.challenge_output_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Unexpected error processing {collection_path.name}: {str(e)}")
            return False
    
    def validate_collection_structure(self, collection_path: Path) -> bool:
        """Validate that collection has required structure"""
        required_files = [
            self.settings.challenge_input_file
        ]
        
        for filename in required_files:
            if not (collection_path / filename).exists():
                self.logger.error(f"Missing required file in {collection_path.name}: {filename}")
                return False
        
        return True
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about available collections"""
        collections_dir = self.settings.get_collections_path()
        collections = self.discover_collections(collections_dir)
        
        stats = {
            'total_collections': len(collections),
            'collections': []
        }
        
        for collection_path in collections:
            try:
                input_file = collection_path / self.settings.challenge_input_file
                challenge_input = self.input_handler.load_challenge_input(input_file)
                documents = challenge_input.get('documents', [])
                
                collection_stats = {
                    'name': collection_path.name,
                    'document_count': len(documents),
                    'has_output': (collection_path / self.settings.challenge_output_file).exists(),
                    'persona': challenge_input.get('persona', {}).get('role', 'Unknown')
                }
                stats['collections'].append(collection_stats)
                
            except Exception as e:
                self.logger.error(f"Error getting stats for {collection_path.name}: {str(e)}")
        
        return stats
