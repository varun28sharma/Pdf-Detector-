from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from pdf_analyzer import analyze_pdf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.urandom(24)  # Required for secure file uploads

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"Server Error: {error}")
    return jsonify({'error': 'Internal server error occurred'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(filepath)
                result = analyze_pdf(filepath)
                # Clean up the uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify(result)
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'error': 'Error processing PDF file'}), 500
        
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 