"""
Download and setup required models - Windows & Docker compatible
"""

import os
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer

def download_models():
    '''Download required models to models directory'''
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Use relative path that works in both environments
    # This will resolve to the correct absolute path automatically
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    models_dir = project_root / 'app' / 'models'
    
    models_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'Using models directory: {models_dir.absolute()}')
    
    # Primary embedding model for Round 1B
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    
    try:
        logger.info(f'Downloading {model_name}...')
        model = SentenceTransformer(model_name)
        
        # Save to models directory
        model_path = models_dir / 'round1b' / 'embedding_model'
        model_path.mkdir(parents=True, exist_ok=True)
        model.save(str(model_path))
        
        logger.info(f'Model saved to {model_path.absolute()}')
        
        # Verify model size
        total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        logger.info(f'Model size: {size_mb:.2f} MB')
        
        if size_mb > 1000:  # 1GB limit
            logger.warning(f'Model size exceeds 1GB limit: {size_mb:.2f} MB')
        else:
            logger.info(f' Model fits within 1GB constraint ({size_mb:.2f} MB)')
        
    except Exception as e:
        logger.error(f'Error downloading model: {str(e)}')
        raise

if __name__ == '__main__':
    download_models()
