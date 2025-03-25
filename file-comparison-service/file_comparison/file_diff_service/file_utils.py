# file_diff_service/file_utils.py
import mimetypes
import magic
import os

def is_text_file(file_path):
    """
    Check if the file is a text-based file.
    
    Supported text-based file types:
    - Plain text (.txt)
    - JSON (.json)
    - CSV (.csv)
    - XML (.xml)
    - Markdown (.md)
    - Configuration files (.ini, .yaml, .yml, .toml)
    - Log files (.log)
    - Source code files (.py, .js, .html, .css, etc.)
    """
    text_mime_types = [
        'text/plain',
        'text/csv',
        'text/xml',
        'text/markdown',
        'text/x-python',
        'text/x-python-script',
        'text/javascript',
        'text/html',
        'text/css',
        'application/json',
        'application/xml',
        'application/x-yaml',
        'application/x-toml',
        'application/x-ini',
        'text/x-log'
    ]
    
    text_extensions = [
        '.txt', '.json', '.csv', '.xml', '.md', 
        '.py', '.js', '.html', '.css', '.log', 
        '.ini', '.yaml', '.yml', '.toml'
    ]
    
    try:
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        
        if any(text_type in file_mime.lower() for text_type in text_mime_types):
            return True
        
        import os
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in text_extensions:
            return True
        
        return False
    
    except Exception as e:
        print(f"Error checking file type: {e}")
        return False

def validate_text_files(file1_path, file2_path):
    """
    This validates both files are text-based.
    
    Returns:
    - (True, None) if both files are text-based
    - (False, error_message) if validation fails
    """
    if not is_text_file(file1_path):
        return False, f"File 1 ({os.path.basename(file1_path)}) is not a text-based file"
    
    if not is_text_file(file2_path):
        return False, f"File 2 ({os.path.basename(file2_path)}) is not a text-based file"
    
    return True, None