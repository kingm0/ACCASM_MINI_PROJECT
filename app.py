from flask import Flask, render_template, request, redirect, url_for, session
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')

image_path = []
latexs = []
extracted_text = []
audio_path = []
image1 = []

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Import model downloader
from model_downloader import ensure_models_exist

# Import your existing Colab code here — wrap into a function
from your_colab_code.main import process_pdf

# Import Gemini integration
from gemini_integration import process_document_with_gemini

def initialize_app():
    """Initialize application and download required models"""
    logger.info("Initializing application...")
    
    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs('static/cropped_images', exist_ok=True)
    os.makedirs('static/outputs', exist_ok=True)
    os.makedirs('static/page_images', exist_ok=True)
    os.makedirs('static/segmentated_images', exist_ok=True)
    
    # Download model files if needed
    ensure_models_exist()
    logger.info("Application initialized successfully")

# Initialize on startup
initialize_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle ML model processing"""
    if 'pdf' not in request.files:
        return "No PDF uploaded", 400
    
    pdf = request.files['pdf']
    if pdf.filename == '':
        return "No file selected", 400
    
    filename = secure_filename(pdf.filename)
    if not filename.lower().endswith('.pdf'):
        return "Invalid file type. Please upload a PDF file.", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    pdf.save(file_path)
    
    session['ml_file_path'] = file_path
    session['processing_type'] = 'ml'
    
    return redirect(url_for('loading')) 
@app.route('/use')  # This route should render 'use.html'
def use():
    return render_template('use.html')
@app.route('/equations')  # This route should render 'use.html'
def equations():
    return render_template('equations.html',
                           image_urls_with_details=image1,
                           texts=extracted_text,
                           audio_urls=audio_path,
                           latex=latexs)

@app.route('/upload-gemini', methods=['POST'])
def upload_gemini():
    """Handle Gemini AI processing"""
    if 'pdf' not in request.files:
        return "No PDF uploaded", 400
    
    pdf = request.files['pdf']
    if pdf.filename == '':
        return "No file selected", 400
    
    filename = secure_filename(pdf.filename)
    if not filename.lower().endswith('.pdf'):
        return "Invalid file type. Please upload a PDF file.", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    pdf.save(file_path)
    
    session['gemini_file_path'] = file_path
    session['processing_type'] = 'gemini'
    
    return redirect(url_for('loading'))

@app.route('/loading')
def loading():
    """Show loading page while processing"""
    processing_type = session.get('processing_type', 'ml')
    
    if processing_type == 'gemini':
        redirect_url = url_for('gemini_results')
    else:
        redirect_url = url_for('process_ml_results')
    
    return render_template('loading.html', redirect_url=redirect_url)

@app.route('/process-ml-results')
def process_ml_results():
    """Process ML model results"""
    file_path = session.get('ml_file_path')
    
    if not file_path:
        return "No file found in session", 400
    
    if not os.path.exists(file_path):
        session.pop('ml_file_path', None)
        session.pop('processing_type', None)
        return "File not found on server", 404
    
    try:
        global image_path, latexs, extracted_text, audio_path, image1
        image_path, latexs, extracted_text, audio_path, image1 = process_pdf(file_path)
        
        session.pop('ml_file_path', None)
        session.pop('processing_type', None)
        
        return render_template('result.html',
                             image_urls=image_path,
                             image_urls_with_details=image1,
                             texts=extracted_text,
                             audio_urls=audio_path,
                             latex=latexs)
    
    except ValueError as e:
        return f"Configuration error: {str(e)}", 500
    except FileNotFoundError as e:
        return f"Required file not found: {str(e)}", 500
    except Exception as e:
        return f"Error processing document: {str(e)}", 500

@app.route('/gemini-results')
def gemini_results():
    """Show Gemini AI analysis results"""
    file_path = session.get('gemini_file_path')
    
    if not file_path:
        return "No file found in session", 400
    
    if not os.path.exists(file_path):
        session.pop('gemini_file_path', None)
        session.pop('processing_type', None)
        return "File not found on server", 404
    
    try:
        analysis_result = process_document_with_gemini(file_path)
        
        page_explanations = analysis_result.get('page_explanations', [])
        page_urls = analysis_result.get('page_urls', [])
        
        session.pop('gemini_file_path', None)
        session.pop('processing_type', None)
        
        return render_template('gemini_result.html',
                             page_explanations=page_explanations,
                             page_urls=page_urls)
    
    except Exception as e:
        return f"Error processing document: {str(e)}", 500

@app.route('/about')
@app.route('/about.html')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/use.html')
def use_html():
    """Use page with .html extension"""
    return render_template('use.html')

@app.route('/index.html')
def index_html():
    """Index page with .html extension"""
    return render_template('index.html')

@app.route('/result')
def result():
    """Show ML model results (existing functionality)"""
    return render_template('result.html',
                           image_urls=image_path,
                           image_urls_with_details=image1,
                           texts=extracted_text,
                           audio_urls=audio_path,
                           latex=latexs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

