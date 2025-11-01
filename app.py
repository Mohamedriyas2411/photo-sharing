from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Storage configuration - Choose between local, Azure, or AWS
STORAGE_TYPE = os.environ.get('STORAGE_TYPE', 'local').lower()  # 'local', 'azure', or 'aws'

# Initialize Storage based on configuration
storage = None
storage_type_name = "Local Storage"

if STORAGE_TYPE == 'aws':
    try:
        from aws_storage_service import AWSS3Storage
        storage = AWSS3Storage(
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1'),
            bucket_name=os.environ.get('AWS_BUCKET_NAME', 'photos')
        )
        storage.create_container()
        storage_type_name = "AWS S3 Storage"
        print("✓ Using AWS S3 Storage")
    except Exception as e:
        print(f"⚠ AWS S3 initialization failed: {e}")
        print("Falling back to Local Storage...")
        STORAGE_TYPE = 'local'

if STORAGE_TYPE == 'azure':
    try:
        from storage_service import AzureBlobStorage
        storage = AzureBlobStorage(
            connection_string=os.environ.get('AZURE_STORAGE_CONNECTION_STRING'),
            container_name=os.environ.get('AZURE_CONTAINER_NAME', 'photos')
        )
        storage.create_container()
        storage_type_name = "Azure Blob Storage"
        print("✓ Using Azure Blob Storage")
    except Exception as e:
        print(f"⚠ Azure Storage initialization failed: {e}")
        print("Falling back to Local Storage...")
        STORAGE_TYPE = 'local'

if STORAGE_TYPE == 'local':
    try:
        from local_storage_service import LocalFileStorage
        storage = LocalFileStorage(
            storage_path='uploads',
            container_name='photos'
        )
        storage.create_container()
        storage_type_name = "Local Storage"
        print("✓ Using Local File Storage")
    except Exception as e:
        print(f"✗ Storage initialization failed: {e}")
        storage = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html', storage_type=storage_type_name)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if storage is None:
        flash('Storage service not configured', 'error')
        return redirect(url_for('index'))
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            
            # Upload to Azure Blob Storage
            blob_url = storage.upload_file(file, filename)
            
            flash(f'File uploaded successfully: {filename}', 'success')
            return redirect(url_for('gallery'))
        except Exception as e:
            flash(f'Upload failed: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP', 'error')
        return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Display all uploaded images"""
    if storage is None:
        flash('Storage service not configured', 'error')
        return redirect(url_for('index'))
    
    try:
        images = storage.list_files()
        return render_template('gallery.html', images=images)
    except Exception as e:
        flash(f'Error loading gallery: {str(e)}', 'error')
        return render_template('gallery.html', images=[])

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete a file from storage"""
    if storage is None:
        return jsonify({'error': 'Storage service not configured'}), 500
    
    try:
        storage.delete_file(filename)
        flash(f'File deleted: {filename}', 'success')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<container>/<filename>')
def serve_uploaded_file(container, filename):
    """Serve uploaded files from local storage"""
    if STORAGE_TYPE == 'local':
        upload_folder = os.path.join('uploads', container)
        return send_from_directory(upload_folder, filename)
    else:
        # For Azure, redirect to blob URL
        return redirect(storage.get_file_url(filename))

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy', 
        'storage_configured': storage is not None,
        'storage_type': storage_type_name
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 16MB', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
