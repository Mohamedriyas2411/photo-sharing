# 📸 Photo Sharing Platform

A cloud-based photo sharing platform built with Python Flask and Azure Blob Storage, designed for secure file storage and retrieval. This application demonstrates container creation, file upload/download operations, and seamless cloud integration.

## ✨ Features

- **Secure Cloud Storage**: Upload images to Azure Blob Storage
- **Container Management**: Automatic container creation and configuration
- **File Operations**: Upload, view, and delete photos
- **Beautiful UI**: Modern, responsive interface with drag-and-drop support
- **Image Gallery**: Browse all uploaded photos with preview functionality
- **File Validation**: Support for PNG, JPG, JPEG, GIF, and WEBP formats
- **Size Management**: Maximum 16MB file size with automatic validation
- **Production Ready**: Configured for deployment on Render.com

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Browser   │ ───> │ Flask App    │ ───> │ Azure Blob      │
│  (Client)   │      │ (Web Server) │      │ Storage         │
└─────────────┘      └──────────────┘      └─────────────────┘
                           │
                           ├── app.py (Routes & Logic)
                           ├── storage_service.py (Azure SDK)
                           └── templates/ (HTML UI)
```

## 📋 Prerequisites

- Python 3.11 or higher
- Azure Storage Account
- Git (for deployment)
- Render.com account (for deployment)

## 🚀 Local Setup

### 1. Clone or Navigate to Project Directory

```powershell
cd "c:\Users\moham\Desktop\photo sharing platform"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Azure Storage credentials:

```env
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
AZURE_CONTAINER_NAME=photos
SECRET_KEY=your-random-secret-key
PORT=5000
```

#### Getting Azure Storage Connection String:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Storage Account (or create one)
3. Go to **Security + networking** → **Access keys**
4. Copy **Connection string** from key1 or key2

### 5. Test Storage Service

Run the storage service test:

```powershell
$env:AZURE_STORAGE_CONNECTION_STRING="your_connection_string"
python storage_service.py
```

This will:
- Create the container if it doesn't exist
- List all files in the container
- Verify the connection works

### 6. Run the Application

```powershell
python app.py
```

Visit: http://localhost:5000

## 📦 Project Structure

```
photo sharing platform/
├── app.py                      # Flask application with routes
├── storage_service.py          # Azure Blob Storage service
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── templates/
    ├── index.html             # Upload page
    └── gallery.html           # Gallery page
```

## 🔧 Core Components

### 1. Storage Service (`storage_service.py`)

Handles all Azure Blob Storage operations:

- **Container Creation**: `create_container()` - Creates container if not exists
- **File Upload**: `upload_file(file_stream, filename)` - Uploads files to blob storage
- **File Retrieval**: `list_files()` - Lists all files with metadata
- **File Download**: `download_file(filename)` - Downloads file content
- **File Deletion**: `delete_file(filename)` - Removes files from storage
- **File Existence**: `file_exists(filename)` - Checks if file exists

### 2. Flask Application (`app.py`)

Web server with the following routes:

- `GET /` - Upload form
- `POST /upload` - Handle file upload
- `GET /gallery` - Display all photos
- `POST /delete/<filename>` - Delete a photo
- `GET /health` - Health check endpoint

### 3. Templates

- **index.html**: Upload interface with drag-and-drop support
- **gallery.html**: Photo gallery with modal preview

## 🌐 Deployment to Render.com

### Step 1: Prepare Git Repository

```powershell
# Initialize git repository
git init
git add .
git commit -m "Initial commit - Photo sharing platform"
```

### Step 2: Push to GitHub

```powershell
# Create repository on GitHub, then:
git remote add origin https://github.com/yourusername/photo-sharing-platform.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Configure environment variables:
   - `AZURE_STORAGE_CONNECTION_STRING`: Your Azure connection string
   - `AZURE_CONTAINER_NAME`: `photos` (or your preferred name)
   - `SECRET_KEY`: Auto-generated by Render
6. Click **Create Web Service**

### Step 4: Verify Deployment

Once deployed, Render will provide a URL like:
```
https://your-app-name.onrender.com
```

Test the endpoints:
- `/` - Upload page
- `/gallery` - Gallery
- `/health` - Health check

## 🧪 Testing

### Test Container Creation

```python
from storage_service import AzureBlobStorage
import os

storage = AzureBlobStorage(
    connection_string=os.environ.get('AZURE_STORAGE_CONNECTION_STRING'),
    container_name='photos'
)

# Create container
storage.create_container()
print("Container created successfully!")
```

### Test File Upload

```python
# Upload a test file
with open('test_image.jpg', 'rb') as f:
    url = storage.upload_file(f, 'test_image.jpg')
    print(f"File uploaded: {url}")
```

### Test File Retrieval

```python
# List all files
files = storage.list_files()
for file in files:
    print(f"Name: {file['name']}, Size: {file['size']} bytes")
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **Connection Strings**: Keep Azure credentials secure
3. **File Validation**: Only allow specific image formats
4. **File Size Limits**: Maximum 16MB per file
5. **HTTPS**: Render provides free SSL certificates
6. **Public Access**: Container is set to 'blob' level (files are public)

## 📊 Storage Operations

### Container Creation
```python
storage.create_container()
```
- Creates container if it doesn't exist
- Sets public access level to 'blob'
- Returns True on success

### File Upload
```python
blob_url = storage.upload_file(file_stream, filename)
```
- Accepts file stream and filename
- Automatically detects content type
- Overwrites existing files
- Returns blob URL

### File Listing
```python
files = storage.list_files()
```
Returns list of dictionaries:
```python
{
    'name': 'photo.jpg',
    'url': 'https://...',
    'size': 1024,
    'created': '2025-11-01 10:30:00',
    'content_type': 'image/jpeg'
}
```

### File Deletion
```python
storage.delete_file(filename)
```
- Deletes file from storage
- Returns True on success
- Returns False if file not found

## 🎨 UI Features

- **Drag & Drop**: Drag files directly to upload area
- **Image Preview**: See images before uploading
- **Responsive Design**: Works on mobile and desktop
- **Modal View**: Click images for full-screen preview
- **File Information**: View size, date, and type
- **Flash Messages**: Success/error notifications

## 🐛 Troubleshooting

### Connection String Issues
```
Error: Azure Storage initialization failed
```
**Solution**: Verify your connection string in `.env` file

### Container Access Issues
```
Error creating container: AuthenticationFailed
```
**Solution**: Check Azure Storage account access keys

### Upload Failures
```
Error uploading file: RequestEntityTooLarge
```
**Solution**: File exceeds 16MB limit - resize or compress

### Render Deployment Issues
```
Build failed: ModuleNotFoundError
```
**Solution**: Ensure `requirements.txt` is correct and committed

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage connection string | Yes | - |
| `AZURE_CONTAINER_NAME` | Container name for photos | No | photos |
| `SECRET_KEY` | Flask secret key | No | dev-secret-key |
| `PORT` | Application port | No | 5000 |

## 🚦 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Upload page |
| `/upload` | POST | Upload file |
| `/gallery` | GET | View gallery |
| `/delete/<filename>` | POST | Delete file |
| `/health` | GET | Health check |

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Private photo albums
- [ ] Image resizing and optimization
- [ ] Thumbnail generation
- [ ] Photo sharing via links
- [ ] Download original files
- [ ] Metadata and EXIF data display
- [ ] Search and filter functionality
- [ ] Batch upload support
- [ ] Photo editing capabilities

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

Created as a cloud application development project demonstrating:
- Azure Blob Storage integration
- Flask web development
- Cloud deployment with Render
- Secure file handling
- Modern UI/UX design

## 📚 Resources

- [Azure Blob Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://render.com/docs)
- [Python Azure SDK](https://github.com/Azure/azure-sdk-for-python)

## 🎯 Learning Objectives Achieved

✅ Container creation and configuration in Azure Blob Storage  
✅ File upload and storage operations  
✅ File retrieval and listing  
✅ Integration with web application  
✅ Secure credential management  
✅ Cloud deployment on Render.com  
✅ Production-ready application structure

---

**Ready to deploy?** Follow the deployment steps above and start sharing photos! 📸
