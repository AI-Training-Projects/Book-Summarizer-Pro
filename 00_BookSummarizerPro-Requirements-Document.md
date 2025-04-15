# BookSummarizerPro - Requirements Document

## Project Overview

BookSummarizerPro is a local Flask web application that enables users to upload PDF or HTML books and generate concise, downloadable summaries using Hugging Face NLP models. The application processes all data locally, making it privacy-focused and eliminating reliance on external APIs.

## Business Purpose

BookSummarizerPro is a local Flask web application that enables entrepreneurs, researchers, and professionals to upload PDF, HTML, or eBooks, and intelligently summarize them into concise, human-readable and downloadable summaries using accurate NLP models from Hugging Face.

The application processes all data locally, making it privacy-focused and eliminating reliance on external APIs.  It ensures high-quality formatting and export options without reliance on cloud APIs.

## Core Features

### 1. File Upload & Processing
- Support for `.pdf` and `.html` file formats
- Secure file handling with appropriate validation
- Text extraction from document files
- Support for large documents (chunking mechanism)

### 2. Summarization Engine
- Multiple model options (configurable):
  - BART (`facebook/bart-large-cnn`) - Default recommended model
  - PEGASUS (`google/pegasus-cnn_dailymail`) - Alternative model
- Token-aware text chunking with configurable settings:
  - Chunk size (default: 800 tokens)
  - Chunk overlap (default: 200 tokens)
- Configurable output-to-input ratio (default: 0.1 or 10%)
- Model caching for performance optimization

### 3. User Interface
- Clean, intuitive web interface
- File upload form with drag-and-drop support
- Summary preview in browser
- Download options for generated summaries
- Flash messages for errors and notifications

### 4. Administration Interface
- Configuration page for modifying settings:
  - Model selection (BART/PEGASUS)
  - Chunk size parameters
  - Summary ratio adjustment
- Basic authentication for admin access

### 5. Output Formats
- Markdown (.md) - Clean text format
- HTML (.html) - Formatted for browser viewing
- PDF (.pdf) - Formatted document for distribution

### 6. Error Handling & Logging
- Comprehensive error logging to `logs/app.log`
- User-friendly error messages
- Fault tolerance for corrupt or invalid inputs
- Exception handling throughout the application

## Technical Requirements

### 1. Technology Stack
- Python 3.10 (managed with Conda)
- Flask web framework
- Hugging Face Transformers library
- PyPDF2 for PDF processing
- BeautifulSoup for HTML processing
- Markdown2 for rendering
- ReportLab for PDF generation

### 2. Environment Management
- Conda environment specification in `environment.yml`
- Avoid pip dependencies when possible, prefer conda packages
- 8-16 GB RAM recommended
- GPU optional but beneficial for performance

### 3. Project Folder and File Structure
```
booksummarizerpro/
├── app.py                    # Main Flask application
├── load_PDF_extract_text.py  # PDF/HTML parsing
├── summarize.py              # Core summarization logic
├── utils.py                  # Utilities (PDF/HTML parsing, chunking)
├── config_manager.py         # Configuration handling
├── templates/
│   ├── index.html            # Frontend upload & preview interface
│   └── admin.html            # Model & chunking config page
├── static/
│   └── style.css             # Styling
├── logs/                     # Log files
├── uploads/                  # Uploaded source documents
├── summaries/                # Generated summaries
├── config/
│   └── settings.json         # Configuration persistence
├── environment.yml           # Conda environment specification
└── README.md                 # Detailed instructions and documentation
├── tests/
│   ├── test_app.py           				# Unit tests for app.py
│   ├── test_summarize.py     				# Unit tests for summarize.py
│   ├── test_utils.py         				# Unit tests for utils.py
│   ├── test_config_manager.py 				# Unit tests for config_manager.py
│   └── test_load_PDF_extract_text.py 	# Unit tests for load PDF extract text

```
