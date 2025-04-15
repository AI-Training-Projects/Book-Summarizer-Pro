# README.md
# BookSummarizerPro

**BookSummarizerPro** is a local Flask web app that lets you upload PDF or HTML books and get concise, downloadable summaries using Hugging Face BART or PEGASUS models. All processing happens locally.

---

## Features
- Upload and summarize `.pdf` or `.html` books.
- Configurable model: `facebook/bart-large-cnn` or `google/pegasus-cnn_dailymail`
- Configurable chunk size, overlap, and output-to-input ratio
- Download summary in `.md`, `.html`, and `.pdf` formats
- Admin interface to configure summarization models and parameters.
- Robust logging and informative error messages to `logs/app.log`

---
## Requirements
- Linux/macOS/Windows
- Python 3.10 (managed with Conda)
- 8–16 GB RAM recommended
- GPU optional but improves performance

---
## Setup Instructions

```bash
# Step 1: Clone the repo (or copy the files)
mkdir booksummarizerpro && cd booksummarizerpro

# Step 2: Create environment
conda env create -f environment.yml
conda activate booksummarizerpro

# Step 3: Run the Flask application:
```bash
python app.py
```


## Application URLs
- **Main Application:** `http://localhost:5000`
- **Admin Configuration:** `http://localhost:5000/appadmin` (Username: `admin`, Password: `Admin123`)
- **Logs:** `http://localhost:5000/logs`


---
## Usage
1. Go to `http://127.0.0.1:5000/`
2. Upload a `.pdf` or `.html` file
3. Wait while it's chunked and summarized
4. Preview the summary
5. Download results in Markdown, HTML, or PDF

---

## Admin Page
- Visit `http://127.0.0.1:5000/admin`
- Set your preferred model, chunk size, overlap, and output-to-input ratio (e.g., 0.1 = 10%)
- Click save to apply settings

---

## Logs
- All logs go to: `logs/app.log`
- Errors during summarization are recorded here

---

## FAQ
**Q: Is this private?**
Yes. All files are processed and stored locally.

**Q: Can it handle large books?**
Yes, documents are chunked automatically.

**Q: What is the default output length ratio?**
10% of the original content length (configurable).

---

## License
MIT License — free for personal and commercial use.

---

Created with love for AI-powered reading tools.
