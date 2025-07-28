"""
File handling utilities with UTF-8 BOM support
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Union

class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_json(self, file_path: Union[str, Path]) -> Dict:
        """Load JSON file with error handling and UTF-8 BOM support"""
        try:
            # First try with utf-8-sig to handle BOM
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except UnicodeDecodeError:
            # Fallback to regular utf-8
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f'Error loading JSON from {file_path}: {str(e)}')
                raise
        except Exception as e:
            self.logger.error(f'Error loading JSON from {file_path}: {str(e)}')
            raise
    
    def save_json(self, data: Dict, file_path: Union[str, Path]) -> bool:
        """Save data to JSON file without BOM"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f'Error saving JSON to {file_path}: {str(e)}')
            return False
    
    def ensure_directory(self, dir_path: Union[str, Path]) -> Path:
        """Ensure directory exists, create if necessary"""
        path_obj = Path(dir_path)
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj
    
    def get_file_list(self, directory: Union[str, Path], pattern: str = '*') -> List[Path]:
        """Get list of files matching pattern"""
        dir_path = Path(directory)
        if not dir_path.exists():
            self.logger.warning(f'Directory does not exist: {directory}')
            return []
        
        return list(dir_path.glob(pattern))
