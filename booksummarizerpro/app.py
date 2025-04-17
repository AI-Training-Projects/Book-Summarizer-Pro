from flask import Flask, render_template, request, send_file, redirect, url_for, flash, Response, stream_with_context
from werkzeug.utils import secure_filename
from summarize import summarize_document
from config_manager import load_config, save_config
from utils import extract_text_from_pdf, extract_text_from_html, save_summary_files, LOG_FILE, get_logs, BASE_DIR
from functools import wraps
import os
import json
import queue
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-for-dev')
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
SUMMARY_FOLDER = os.path.join(BASE_DIR, "summaries")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

# Progress tracking
progress_queues = {}

# Admin credentials from environment variables
USERNAME = os.getenv('ADMIN_USERNAME')
PASSWORD = os.getenv('ADMIN_PASSWORD')

if not USERNAME or not PASSWORD:
    app.logger.error("ADMIN_USERNAME and ADMIN_PASSWORD must be set in environment variables")
    raise RuntimeError("Admin credentials not configured. Set ADMIN_USERNAME and ADMIN_PASSWORD in .env file")

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def update_progress(progress):
    task_id = threading.get_ident()
    if task_id in progress_queues:
        progress_queues[task_id].put(progress)

@app.route('/progress/<int:task_id>')
def progress_stream(task_id):
    def generate():
        q = progress_queues.get(task_id)
        if not q:
            yield f"data: {json.dumps({'progress': 100, 'status': 'complete'})}\n\n"
            return

        while True:
            try:
                progress = q.get(timeout=1)
                yield f"data: {json.dumps({'progress': progress, 'status': 'processing'})}\n\n"
                if progress >= 100:
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'progress': -1, 'status': 'waiting'})}\n\n"

        del progress_queues[task_id]

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part in the request.", "error")
            return redirect(request.url)

        file = request.files['file']
        if not file or file.filename == '':
            flash("No file selected.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(filepath)
            app.logger.info(f"File uploaded successfully: {filename}")

            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(filepath)
                app.logger.info(f"Successfully extracted text from PDF: {filename}")
            elif filename.lower().endswith((".html", ".htm")):
                text = extract_text_from_html(filepath)
                app.logger.info(f"Successfully extracted text from HTML: {filename}")
            else:
                raise ValueError("Unsupported file type. Only PDF and HTML files are supported.")

            config = load_config(CONFIG_PATH)
            app.logger.info("Loaded configuration successfully")

            # Set up progress tracking
            task_id = threading.get_ident()
            progress_queues[task_id] = queue.Queue()
            app.progress_callback = update_progress

            app.logger.info("Starting document summarization")
            summary, out_dir = summarize_document(text, config, SUMMARY_FOLDER)
            app.logger.info("Document summarization completed")

            download_links = save_summary_files(summary, out_dir)
            app.logger.info(f"Summary files saved successfully in {out_dir}")

            return render_template("index.html",
                                summary=summary,
                                links=download_links,
                                task_id=task_id)

        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(request.url)
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
                app.logger.info(f"Cleaned up uploaded file: {filename}")

    return render_template("index.html")

@app.route("/appadmin", methods=["GET", "POST"])
@requires_auth
def admin():
    try:
        config = load_config(CONFIG_PATH)
        if request.method == "POST":
            config['model'] = request.form['model']
            config['chunk_size'] = int(request.form['chunk_size'])
            config['chunk_overlap'] = int(request.form['chunk_overlap'])
            config['summary_ratio'] = float(request.form['summary_ratio'])
            save_config(config, CONFIG_PATH)
            app.logger.info("Configuration updated successfully")
            flash("Configuration updated successfully.", "success")
            return redirect(url_for("admin"))
    except Exception as e:
        app.logger.error(f"Error in admin page: {str(e)}")
        flash(f"Error loading/saving configuration: {str(e)}", "error")
        config = {'model': 'bart', 'chunk_size': 1024, 'chunk_overlap': 200, 'summary_ratio': 0.3}

    return render_template("admin.html", config=config)

@app.route("/logs")
@requires_auth
def logs():
    log_content = get_logs()
    return render_template("logs.html", logs=log_content)

@app.route("/download/<path:filename>")
def download_file(filename):
    try:
        app.logger.info(f"Downloading file: {filename}")
        return send_file(filename, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error downloading file: {str(e)}")
        flash("Error downloading file.", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    # Set up logging
    import logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        encoding='utf-8'  # Explicitly set UTF-8 encoding
    )
    app.logger.info("Application started")
    app.run(debug=True)