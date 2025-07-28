"""
Embedding generation for semantic similarity
"""

import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union
from pathlib import Path

class EmbeddingGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # ✅ FIXED: Use local model path instead of downloading
        local_model_path = '/app/app/models/round1b/embedding_model'
        
        if Path(local_model_path).exists():
            self.model_path = local_model_path
            self.logger.info(f'Using local model at: {local_model_path}')
        else:
            self.logger.error(f'Local model not found at: {local_model_path}')
            raise FileNotFoundError(f'Embedding model not found at {local_model_path}')
            
        self.model = None
        self._load_model()
    
    def _load_model(self):
        '''Load the sentence transformer model from local path'''
        try:
            # Load from local path with explicit device setting
            self.model = SentenceTransformer(self.model_path, device='cpu')
            self.logger.info(f'Successfully loaded model from: {self.model_path}')
        except Exception as e:
            self.logger.error(f'Failed to load model from {self.model_path}: {str(e)}')
            raise
    
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        '''Generate embeddings for a list of texts'''
        if not self.model:
            raise RuntimeError('Model not loaded')
        
        # Clean and preprocess texts
        clean_texts = [self._preprocess_text(text) for text in texts]
        
        # Generate embeddings
        embeddings = self.model.encode(clean_texts, normalize_embeddings=True)
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        '''Generate embedding for a single text'''
        return self.encode_texts([text])[0]
    
    def _preprocess_text(self, text: str) -> str:
        '''Clean and preprocess text for embedding'''
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Limit length (models have token limits)
        if len(text) > 500:
            text = text[:500] + '...'
        
        return text
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        '''Calculate cosine similarity between two embeddings'''
        return float(np.dot(embedding1, embedding2))
