"""
Service 1B Configuration Settings
Persona-Driven Document Intelligence Service
"""

import os
from typing import Optional, List
from pathlib import Path

class Settings:
    def __init__(self):
        # Service identification
        self.service: str = os.getenv('SERVICE', '1B')
        self.round: str = os.getenv('ROUND', 'round1b')
        
        # Directory paths for Service 1B
        self.collections_dir: str = '/app/collections'
        self.models_dir: str = '/app/models'
        self.logs_dir: str = '/app/logs'
        
        # Logging
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')
        
        # Embedding Model Configuration
        self.embedding_model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'
        self.embedding_model_path: str = '/app/models/round1b/embedding_model'
        self.embedding_dimension: int = 384
        
        # Persona-Driven Analysis Settings
        self.supported_personas: List[str] = [
            'QA Engineer',
            'Data Scientist', 
            'Digital Transformation Consultant',
            'Product Manager',
            'Software Engineer'
        ]
        
        # Query and Analysis Configuration
        self.max_results_per_query: int = 10
        self.relevance_threshold: float = 0.3
        self.query_expansion_enabled: bool = True
        
        # Performance settings for Service 1B
        self.max_memory_mb: int = 1024  # Hackathon limit ≤1GB
        self.timeout_seconds: int = 60   # Max 60 seconds per collection (hackathon req)
        self.max_concurrent_collections: int = 3
        
        # Collection Processing Settings
        self.min_collections: int = 3
        self.max_collections: int = 10
        self.min_pdfs_per_collection: int = 3
        self.max_pdfs_per_collection: int = 10
        
        # Similarity Search Configuration
        self.similarity_search_top_k: int = 20
        self.persona_weight: float = 0.3      # 30% persona relevance
        self.query_weight: float = 0.7        # 70% query relevance
        
        # Output Format Settings
        self.output_format: str = 'json'
        self.include_confidence_scores: bool = True
        self.include_document_metadata: bool = True
        
        # Error handling
        self.continue_on_error: bool = True
        self.max_retries: int = 2
        
        # Challenge 1B Specific
        self.challenge_input_file: str = 'challenge1b_input.json'
        self.challenge_output_file: str = 'challenge1b_output.json'
        
    def get_collections_path(self) -> Path:
        """Get collections directory as Path object"""
        return Path(self.collections_dir)
    
    def get_models_path(self) -> Path:
        """Get models directory as Path object"""
        return Path(self.models_dir)
    
    def get_logs_path(self) -> Path:
        """Get logs directory as Path object"""
        return Path(self.logs_dir)
    
    def get_embedding_model_path(self) -> Path:
        """Get embedding model directory as Path object"""
        return Path(self.embedding_model_path)
    
    def validate_directories(self) -> bool:
        """Ensure required directories exist"""
        try:
            self.get_collections_path().mkdir(parents=True, exist_ok=True)
            self.get_logs_path().mkdir(parents=True, exist_ok=True)
            # Models directory should already exist with pre-trained embeddings
            return True
        except Exception:
            return False
    
    def get_collection_input_file(self, collection_name: str) -> str:
        """Generate input filename for a collection"""
        return f"{collection_name}/{self.challenge_input_file}"
    
    def get_collection_output_file(self, collection_name: str) -> str:
        """Generate output filename for a collection"""
        return f"{collection_name}/{self.challenge_output_file}"
    
    def is_persona_supported(self, persona: str) -> bool:
        """Check if persona is supported"""
        return persona in self.supported_personas
    
    def get_persona_queries(self, persona: str) -> List[str]:
        """Get persona-specific query expansions"""
        persona_queries = {
            'QA Engineer': [
                'testing procedures', 'test cases', 'quality assurance',
                'bugs', 'defects', 'validation', 'verification'
            ],
            'Data Scientist': [
                'data analysis', 'machine learning', 'statistics',
                'algorithms', 'models', 'datasets', 'analytics'
            ],
            'Digital Transformation Consultant': [
                'digital strategy', 'transformation', 'technology adoption',
                'process improvement', 'automation', 'innovation'
            ],
            'Product Manager': [
                'product requirements', 'roadmap', 'features',
                'user experience', 'business value', 'strategy'
            ],
            'Software Engineer': [
                'code', 'development', 'programming', 'architecture',
                'implementation', 'technical specifications', 'APIs'
            ]
        }
        return persona_queries.get(persona, [])
