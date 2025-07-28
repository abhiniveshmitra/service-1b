"""
Main service for Round 1B - Persona-driven relevance ranking
Legacy support for queries.json format
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

from config.settings import Settings  # ADD THIS IMPORT
from services.round1b.document_loader import DocumentLoader
from services.round1b.persona_matcher import PersonaMatcher
from utils.file_handler import FileHandler
from utils.logger import setup_logger

class RelevanceRanker:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.settings = Settings()  # ADD THIS
        self.document_loader = DocumentLoader()
        self.persona_matcher = PersonaMatcher()
        self.file_handler = FileHandler()
    
    def process(self):
        """Legacy processing pipeline for Round 1B (queries.json format)"""
        self.logger.info("Starting Legacy RelevanceRanker (queries.json format)")
        
        # ✅ FIXED - Use collections directory for Service 1B
        collections_dir = self.settings.get_collections_path()
        
        if not collections_dir.exists():
            self.logger.error(f"Collections directory not found: {collections_dir}")
            return
        
        # Look for legacy queries.json files in collection directories
        query_files_found = []
        
        for collection_dir in collections_dir.iterdir():
            if collection_dir.is_dir():
                queries_file = collection_dir / 'queries.json'
                if queries_file.exists():
                    query_files_found.append((collection_dir, queries_file))
        
        if not query_files_found:
            self.logger.warning("No legacy queries.json files found in any collection")
            self.logger.info("This is expected - modern Service 1B uses challenge1b_input.json format")
            return
        
        self.logger.info(f"Found {len(query_files_found)} legacy queries.json files")
        
        # Process each queries.json file
        for collection_dir, queries_file in query_files_found:
            try:
                self.logger.info(f"Processing legacy queries from: {collection_dir.name}")
                
                queries = self.file_handler.load_json(queries_file)
                self.logger.info(f"Loaded {len(queries)} queries from {queries_file.name}")
                
                # Process each query in the collection
                for query_id, query_data in queries.items():
                    try:
                        result = self.rank_for_query(query_data, collection_dir)
                        output_file = collection_dir / f'relevance_{query_id}.json'
                        
                        if self.file_handler.save_json(result, output_file):
                            self.logger.info(f"✅ Processed query {query_id} in {collection_dir.name}")
                        else:
                            self.logger.error(f"❌ Failed to save query {query_id}")
                        
                    except Exception as e:
                        self.logger.error(f"❌ Error processing query {query_id}: {str(e)}")
                        import traceback
                        self.logger.error(traceback.format_exc())
                        
            except Exception as e:
                self.logger.error(f"❌ Error processing queries from {collection_dir.name}: {str(e)}")
    
    def rank_for_query(self, query_data: Dict, collection_dir: Path) -> Dict:
        """Rank documents for a specific persona query (legacy format)"""
        job_role = query_data.get('job_role', '')
        search_query = query_data.get('query', '')
        documents = query_data.get('documents', [])
        
        self.logger.debug(f"Ranking for persona: {job_role}, query: {search_query[:50]}...")
        
        all_results = []
        
        for doc_info in documents:
            # ✅ FIXED - Look for outline files in same collection directory
            outline_filename = doc_info.get('outline_file', f"{doc_info['name'].replace('.pdf', '_outline.json')}")
            outline_path = collection_dir / outline_filename
            
            self.logger.debug(f"Looking for outline: {outline_path}")
            
            if outline_path.exists():
                try:
                    # Load document outline
                    outline_data = self.file_handler.load_json(outline_path)
                    sections = outline_data.get('outline', [])
                    
                    if not sections:
                        self.logger.warning(f"No sections found in {outline_filename}")
                        continue
                    
                    # Add document metadata to sections
                    for section in sections:
                        section['document'] = doc_info['name']
                        section['collection'] = collection_dir.name
                    
                    # Rank sections using PersonaMatcher
                    ranked_sections = self.persona_matcher.rank_sections(
                        sections, job_role, search_query
                    )
                    
                    # Format results
                    doc_results = {
                        'document': doc_info['name'],
                        'total_sections': len(ranked_sections),
                        'top_matches': [
                            {
                                'section': {
                                    'text': section[0].get('text', ''),
                                    'level': section[0].get('level', ''),
                                    'page': section[0].get('page', 1)
                                },
                                'relevance_score': round(section[1], 4),
                                'rank': idx + 1
                            }
                            for idx, section in enumerate(ranked_sections[:10])
                        ]
                    }
                    all_results.append(doc_results)
                    
                    self.logger.info(f"   Processed {len(sections)} sections from {doc_info['name']}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing document {doc_info['name']}: {str(e)}")
            else:
                self.logger.warning(f"Outline file not found: {outline_path}")
        
        return {
            'query_id': query_data.get('id', ''),
            'job_role': job_role,
            'search_query': search_query,
            'results': all_results,
            'metadata': {
                'total_documents': len(documents),
                'successful_documents': len(all_results),
                'collection': collection_dir.name,
                'processing_method': 'legacy_queries_json'
            }
        }
    
    def process_single_query(self, query_data: Dict, collection_dir: Path) -> Dict:
        """Process a single query - helper method"""
        try:
            return self.rank_for_query(query_data, collection_dir)
        except Exception as e:
            self.logger.error(f"Error processing single query: {str(e)}")
            return {
                'error': str(e),
                'query_id': query_data.get('id', 'unknown')
            }
