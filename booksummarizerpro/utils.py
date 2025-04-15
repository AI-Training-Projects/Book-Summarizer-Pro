# Utilities (PDF/HTML parsing, chunking)

import os
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from markdown2 import markdown
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Get the base directory for the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)
# Create log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'a').close()

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() for page in reader.pages)

def extract_text_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup.get_text()

def chunk_text(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

def save_summary_files(summary, folder):
    os.makedirs(folder, exist_ok=True)
    md_path = os.path.join(folder, 'summary.md')
    html_path = os.path.join(folder, 'summary.html')
    pdf_path = os.path.join(folder, 'summary.pdf')

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(summary)

    html_content = markdown(summary)
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = [Paragraph(p, styles['Normal']) for p in summary.split('\n\n')]
    doc.build(story)

    return {'Markdown': md_path, 'HTML': html_path, 'PDF': pdf_path}

def get_logs():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading log file: {str(e)}"
