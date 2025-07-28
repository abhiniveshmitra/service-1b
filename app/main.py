"""
Service 1B: Persona-Driven Document Intelligence
Adobe Hackathon 2025 - Challenge 1B Compliant
"""

import sys
import os
import time
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from config.settings import Settings
from services.round1b.collection_processor import CollectionProcessor
from utils.logger import setup_logger
from utils.json_validator import JSONValidator

def main():
    """Main application entry point for Service 1B - Persona-Driven Document Intelligence"""
    logger = setup_logger()
    settings = Settings()
    validator = JSONValidator()
    
    logger.info("Starting Adobe Hackathon Service 1B - Persona-Driven Document Intelligence")
    logger.info(f"Service: {getattr(settings, 'service', '1B')}")
    logger.info(f"Round: {getattr(settings, 'round', 'round1b')}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    try:
        # Validate directories exist
        if not settings.validate_directories():
            logger.error("Failed to create required directories")
            sys.exit(1)
        
        logger.info("Initializing Challenge 1B Multi-Collection Processing")
        collection_processor = CollectionProcessor()
        
        # Get collections directory from settings
        collections_dir = settings.get_collections_path()
        
        logger.info(f"Collections directory: {collections_dir.absolute()}")
        
        if not collections_dir.exists():
            logger.error(f"Collections directory not found: {collections_dir}")
            logger.info("Please ensure collections directory exists with challenge1b_input.json files")
            sys.exit(1)
        
        # Get collection statistics
        stats = collection_processor.get_collection_stats()
        logger.info(f"Found {stats['total_collections']} collections to process")
        
        if stats['total_collections'] == 0:
            logger.warning("No collections found with challenge1b_input.json files")
            logger.info(f"Expected structure: {collections_dir}/Collection_Name/challenge1b_input.json")
            return
        
        # Log collection details
        for collection_info in stats['collections']:
            logger.info(f"  📁 {collection_info['name']}: {collection_info['document_count']} documents, Persona: {collection_info['persona']}")
        
        start_time = time.time()
        
        # Process all collections
        collection_processor.process_all_collections(collections_dir)
        
        processing_time = time.time() - start_time
        
        # Validate outputs
        logger.info("Validating generated outputs...")
        validation_summary = validate_all_outputs(collections_dir, validator, logger)
        
        # Final summary
        logger.info("=" * 60)
        logger.info(f"Service 1B processing completed")
        logger.info(f"⏱️  Total processing time: {processing_time:.2f}s")
        logger.info(f"📊 Collections processed: {stats['total_collections']}")
        logger.info(f"✅ Valid outputs: {validation_summary['valid']}")
        if validation_summary['invalid'] > 0:
            logger.warning(f"❌ Invalid outputs: {validation_summary['invalid']}")
        
        # Check timing compliance (≤60 seconds per collection average)
        avg_time_per_collection = processing_time / max(stats['total_collections'], 1)
        if avg_time_per_collection > settings.timeout_seconds:
            logger.warning(f"Average processing time {avg_time_per_collection:.2f}s exceeds {settings.timeout_seconds}s limit")
        else:
            logger.info(f"✅ Average processing time: {avg_time_per_collection:.2f}s per collection")
        
    except Exception as e:
        logger.error(f"Service 1B critical error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

def validate_all_outputs(collections_dir: Path, validator: JSONValidator, logger) -> dict:
    """Validate all generated challenge1b_output.json files"""
    valid_count = 0
    invalid_count = 0
    
    for collection_dir in collections_dir.iterdir():
        if collection_dir.is_dir():
            output_file = collection_dir / 'challenge1b_output.json'
            if output_file.exists():
                try:
                    is_valid, errors = validator.validate_output_file(output_file)
                    if is_valid:
                        valid_count += 1
                        logger.info(f"✅ {collection_dir.name}: Output validation passed")
                    else:
                        invalid_count += 1
                        logger.error(f"❌ {collection_dir.name}: Output validation failed")
                        for error in errors[:3]:  # Show first 3 errors
                            logger.error(f"   - {error}")
                except Exception as e:
                    invalid_count += 1
                    logger.error(f"❌ {collection_dir.name}: Validation error - {str(e)}")
    
    return {'valid': valid_count, 'invalid': invalid_count}

if __name__ == "__main__":
    main()
