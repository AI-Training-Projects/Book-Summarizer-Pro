import os
import logging
from datetime import datetime
import json

# Setup logging
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'project_structure_creation_{timestamp}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def create_directory(path):
    """Create directory if it doesn't exist and log the action."""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logging.info(f"Created directory: {path}")
        else:
            logging.info(f"Directory already exists (skipped): {path}")
    except Exception as e:
        logging.error(f"Error creating directory {path}: {str(e)}")

def create_file(path, content=""):
    """Create file if it doesn't exist and log the action."""
    try:
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Created file: {path}")
        else:
            logging.info(f"File already exists (skipped): {path}")
    except Exception as e:
        logging.error(f"Error creating file {path}: {str(e)}")

def main():
    # Project root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(root_dir, 'booksummarizerpro')

    # Create main project directory
    create_directory(project_dir)

    # Create subdirectories
    directories = [
        os.path.join(project_dir, 'templates'),
        os.path.join(project_dir, 'static'),
        os.path.join(project_dir, 'logs'),
        os.path.join(project_dir, 'uploads'),
        os.path.join(project_dir, 'summaries'),
        os.path.join(project_dir, 'config'),
    ]

    for directory in directories:
        create_directory(directory)

    # Create files with basic content
    files = {
        'app.py': '# Main Flask application\nfrom flask import Flask\n\napp = Flask(__name__)\n',
        'summarize.py': '# Core summarization logic\n',
        'utils.py': '# Utilities (PDF/HTML parsing, chunking)\n',
        'config_manager.py': '# Configuration handling\n',
        'templates/index.html': '<!-- Frontend upload & preview interface -->\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Book Summarizer Pro</title>\n</head>\n<body>\n    <h1>Book Summarizer Pro</h1>\n</body>\n</html>',
        'templates/admin.html': '<!-- Model & chunking config page -->\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Admin - Book Summarizer Pro</title>\n</head>\n<body>\n    <h1>Admin Configuration</h1>\n</body>\n</html>',
        'static/style.css': '/* Styling */\nbody {\n    font-family: Arial, sans-serif;\n}',
        'config/settings.json': '{\n    "version": "1.0",\n    "settings": {}\n}',
        'environment.yml': 'name: booksummarizerpro\nchannels:\n  - defaults\n  - conda-forge\n',
        'README.md': '# Book Summarizer Pro\n\nDetailed instructions and documentation will go here.\n'
    }

    for file_path, content in files.items():
        create_file(os.path.join(project_dir, file_path), content)

    logging.info("Project structure creation completed!")

if __name__ == "__main__":
    logging.info("Starting project structure creation...")
    main()
