"""
Collection setup and validation script
"""

import json
import shutil
from pathlib import Path

def setup_collections():
    """Setup collection directories and copy outline files"""
    
    collections_dir = Path('./collections')
    app_output_dir = Path('./app/output')
    
    print("Setting up Challenge 1B collections...")
    
    # Collection 1: Software Testing
    collection1 = collections_dir / 'Collection 1'
    collection1.mkdir(parents=True, exist_ok=True)
    
    # Copy outline file for Collection 1
    outline_source = app_output_dir / 'E0CCG5S312_outline.json'
    if outline_source.exists():
        outline_dest = collection1 / 'E0CCG5S312_outline.json'
        shutil.copy2(outline_source, outline_dest)
        print(f"Copied outline to {outline_dest}")
    
    # Collection 2: Digital Library
    collection2 = collections_dir / 'Collection 2'
    collection2.mkdir(parents=True, exist_ok=True)
    
    # Copy outline file for Collection 2
    outline_source2 = app_output_dir / 'E0H1CM114_outline.json'
    if outline_source2.exists():
        outline_dest2 = collection2 / 'E0H1CM114_outline.json'
        shutil.copy2(outline_source2, outline_dest2)
        print(f"Copied outline to {outline_dest2}")
    
    print("Collection setup completed!")
    
    # Validate setup
    for collection in [collection1, collection2]:
        input_file = collection / 'challenge1b_input.json'
        if input_file.exists():
            print(f" {collection.name}: Input file ready")
        else:
            print(f" {collection.name}: Missing input file")

if __name__ == "__main__":
    setup_collections()
