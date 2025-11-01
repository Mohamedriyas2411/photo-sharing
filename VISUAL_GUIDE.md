# 🎨 Photo Sharing Platform - Visual Guide

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHOTO SHARING PLATFORM                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│              │         │              │         │              │
│   Browser    │◄───────►│  Flask App   │◄───────►│    Azure     │
│  (Client)    │  HTTP   │ (Render.com) │  SDK    │ Blob Storage │
│              │         │              │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
      ▲                        │                         │
      │                        │                         │
      │                  ┌─────▼─────┐            ┌─────▼─────┐
      │                  │Templates  │            │Container  │
      │                  ├───────────┤            │"photos"   │
      └──────────────────│index.html │            ├───────────┤
                         │gallery.html│           │photo1.jpg │
                         └───────────┘            │photo2.png │
                                                  │photo3.gif │
                                                  └───────────┘
```

## 🔄 Data Flow Diagrams

### Upload Process

```
1. USER ACTION
   └─► Select/Drag image to upload area
          │
          ▼
2. CLIENT VALIDATION
   ├─► Check file type (PNG/JPG/JPEG/GIF/WEBP)
   ├─► Check file size (max 16MB)
   └─► Show preview
          │
          ▼
3. SUBMIT TO SERVER
   └─► POST /upload with file data
          │
          ▼
4. SERVER VALIDATION
   ├─► Verify file exists
   ├─► Check allowed extensions
   └─► Secure filename
          │
          ▼
5. AZURE STORAGE
   ├─► storage.upload_file(file, filename)
   ├─► Set content-type
   └─► Save to blob
          │
          ▼
6. RESPONSE
   ├─► Success: Flash message + redirect to gallery
   └─► Error: Flash error + redirect to upload
```

### Retrieval Process

```
1. USER REQUESTS GALLERY
   └─► GET /gallery
          │
          ▼
2. SERVER QUERIES AZURE
   └─► storage.list_files()
          │
          ▼
3. AZURE RETURNS METADATA
   ├─► File names
   ├─► File URLs
   ├─► File sizes
   └─► Creation dates
          │
          ▼
4. SERVER RENDERS TEMPLATE
   └─► gallery.html with image data
          │
          ▼
5. BROWSER DISPLAYS GALLERY
   ├─► Grid of image cards
   ├─► Direct URLs to Azure blobs
   └─► Click for full preview
```

### Delete Process

```
1. USER CLICKS DELETE
   └─► Confirmation prompt
          │
          ▼
2. AJAX REQUEST
   └─► POST /delete/<filename>
          │
          ▼
3. SERVER DELETES FROM AZURE
   └─► storage.delete_file(filename)
          │
          ▼
4. AZURE REMOVES BLOB
   └─► File deleted from container
          │
          ▼
5. RESPONSE TO CLIENT
   ├─► Success: Reload page
   └─► Error: Show error message
```

## 🗂️ File Structure Visualization

```
📁 photo sharing platform/
│
├── 🐍 app.py                  [Main Flask application]
│   ├── Routes: /, /upload, /gallery, /delete, /health
│   ├── File validation
│   └── Error handling
│
├── ☁️ storage_service.py      [Azure Blob Storage service]
│   ├── Class: AzureBlobStorage
│   ├── create_container()
│   ├── upload_file()
│   ├── list_files()
│   ├── download_file()
│   ├── delete_file()
│   └── file_exists()
│
├── 📦 requirements.txt        [Python dependencies]
│   ├── Flask==3.0.0
│   ├── azure-storage-blob==12.19.0
│   ├── python-dotenv==1.0.0
│   └── gunicorn==21.2.0
│
├── 🚀 render.yaml            [Render deployment config]
│   ├── Build command
│   ├── Start command
│   └── Environment variables
│
├── 📁 templates/
│   ├── 🎨 index.html         [Upload page]
│   │   ├── Drag-and-drop zone
│   │   ├── File preview
│   │   └── Upload button
│   │
│   └── 🖼️ gallery.html       [Photo gallery]
│       ├── Image grid
│       ├── Modal preview
│       └── Delete buttons
│
├── ⚙️ setup.py               [Environment setup script]
├── 🎬 demo_storage.py        [Storage operations demo]
│
├── 📄 .env.example           [Environment template]
├── 🚫 .gitignore             [Git ignore rules]
│
├── 📖 README.md              [Full documentation]
├── ⚡ QUICKSTART.md          [Quick setup guide]
├── 🚀 DEPLOYMENT.md          [Render deployment guide]
└── 📊 PROJECT_SUMMARY.md     [Project overview]
```

## 🔐 Security Flow

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                       │
└─────────────────────────────────────────────────────────┘

1. CLIENT SIDE
   ├─► File type validation
   ├─► File size check
   └─► Preview before upload
          │
          ▼
2. SERVER SIDE
   ├─► Werkzeug secure_filename()
   ├─► Extension whitelist check
   ├─► File size limit (16MB)
   └─► Content-type validation
          │
          ▼
3. TRANSPORT
   ├─► HTTPS encryption (Render SSL)
   └─► Secure headers
          │
          ▼
4. AZURE STORAGE
   ├─► Connection string authentication
   ├─► Access key protected
   └─► Container-level permissions
          │
          ▼
5. ENVIRONMENT
   ├─► .env file (not committed)
   ├─► Environment variables
   └─► Secret key for Flask sessions
```

## 📱 User Interface Flow

```
HOME PAGE (/)
┌─────────────────────────────────────┐
│  📸 Photo Share                     │
│  Upload and share your memories     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │     ☁️                       │   │
│  │  Click to upload or drag     │   │
│  │  PNG, JPG, JPEG, GIF, WEBP   │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Upload Photo]                     │
│  [View Gallery]                     │
└─────────────────────────────────────┘
          │
          ├─── Select File ───┐
          │                   │
          ▼                   ▼
    ┌─────────┐         Preview Image
    │ Upload  │              │
    └─────────┘              │
          │                  │
          └──────────┬───────┘
                     ▼
               Upload Success
                     │
                     ▼
GALLERY PAGE (/gallery)
┌─────────────────────────────────────┐
│  📸 Photo Gallery                   │
│  Your shared memories               │
│                                     │
│  [➕ Upload New Photo]              │
│                                     │
│  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │img1 │  │img2 │  │img3 │         │
│  │📷   │  │📷   │  │📷   │         │
│  │🗑️  │  │🗑️  │  │🗑️  │         │
│  └─────┘  └─────┘  └─────┘         │
│                                     │
│  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │img4 │  │img5 │  │img6 │         │
│  │📷   │  │📷   │  │📷   │         │
│  │🗑️  │  │🗑️  │  │🗑️  │         │
│  └─────┘  └─────┘  └─────┘         │
└─────────────────────────────────────┘
          │
          ├─── Click Image ───► Full Screen Preview
          │
          └─── Click Delete ──► Confirm ──► Delete
```

## ⚙️ Configuration Flow

```
DEVELOPMENT SETUP
┌─────────────────────────────────────┐
│ 1. Install Python 3.11+             │
├─────────────────────────────────────┤
│ 2. Install dependencies             │
│    pip install -r requirements.txt  │
├─────────────────────────────────────┤
│ 3. Create .env from .env.example    │
│    Add Azure connection string      │
├─────────────────────────────────────┤
│ 4. Run setup.py                     │
│    Validates environment            │
│    Creates container                │
├─────────────────────────────────────┤
│ 5. Run app.py                       │
│    python app.py                    │
├─────────────────────────────────────┤
│ 6. Open http://localhost:5000       │
└─────────────────────────────────────┘

PRODUCTION DEPLOYMENT
┌─────────────────────────────────────┐
│ 1. Push code to GitHub              │
│    git push origin main             │
├─────────────────────────────────────┤
│ 2. Connect to Render.com            │
│    Link GitHub repository           │
├─────────────────────────────────────┤
│ 3. Configure environment vars       │
│    AZURE_STORAGE_CONNECTION_STRING  │
│    AZURE_CONTAINER_NAME             │
│    SECRET_KEY                       │
├─────────────────────────────────────┤
│ 4. Deploy                           │
│    Render auto-builds & deploys     │
├─────────────────────────────────────┤
│ 5. Access via Render URL            │
│    https://your-app.onrender.com    │
└─────────────────────────────────────┘
```

## 🔄 Storage Operations

```
CREATE CONTAINER
┌──────────────────────────────────┐
│ storage.create_container()       │
│   ├─► Check if exists            │
│   ├─► Create if not              │
│   ├─► Set public access (blob)   │
│   └─► Return success             │
└──────────────────────────────────┘

UPLOAD FILE
┌──────────────────────────────────┐
│ storage.upload_file(file, name)  │
│   ├─► Get blob client            │
│   ├─► Detect content-type        │
│   ├─► Upload stream              │
│   ├─► Overwrite if exists        │
│   └─► Return blob URL            │
└──────────────────────────────────┘

LIST FILES
┌──────────────────────────────────┐
│ storage.list_files()             │
│   ├─► Query container blobs      │
│   ├─► Extract metadata           │
│   │   ├─► Name                   │
│   │   ├─► URL                    │
│   │   ├─► Size                   │
│   │   ├─► Created date           │
│   │   └─► Content-type           │
│   └─► Return list                │
└──────────────────────────────────┘

DELETE FILE
┌──────────────────────────────────┐
│ storage.delete_file(filename)    │
│   ├─► Get blob client            │
│   ├─► Check if exists            │
│   ├─► Delete blob                │
│   └─► Return success             │
└──────────────────────────────────┘
```

## 🎯 Request/Response Examples

### Upload Request
```
POST /upload HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="photo.jpg"
Content-Type: image/jpeg

[binary data]
------WebKitFormBoundary--
```

### Upload Response (Success)
```
HTTP/1.1 302 Found
Location: /gallery
Set-Cookie: session=...

Flash: "File uploaded successfully: photo.jpg"
```

### Gallery Request
```
GET /gallery HTTP/1.1
Host: localhost:5000
```

### Gallery Response
```
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <body>
    <div class="gallery">
      <div class="photo-card">
        <img src="https://your-storage.blob.core.windows.net/photos/photo.jpg">
        ...
      </div>
    </div>
  </body>
</html>
```

## 📊 Performance Metrics

```
OPERATION           | TIME      | NOTES
--------------------|-----------|---------------------------
Container Create    | 100-500ms | One-time operation
File Upload (1MB)   | 1-3s      | Depends on network
File Upload (10MB)  | 5-15s     | Depends on network
List Files (50)     | 200-800ms | Cached by Azure
Delete File         | 100-300ms | Quick operation
Page Load (Gallery) | 500ms-2s  | First load slower
Image Preview       | Instant   | Direct Azure URL
```

## 🎨 UI Components

```
UPLOAD PAGE COMPONENTS
┌─────────────────────────────────┐
│ Header                          │
│   ├─► Title: "📸 Photo Share"   │
│   └─► Subtitle                  │
├─────────────────────────────────┤
│ Flash Messages (if any)         │
│   ├─► Success (green)           │
│   └─► Error (red)               │
├─────────────────────────────────┤
│ Upload Area                     │
│   ├─► Drag-drop zone            │
│   ├─► Click to browse           │
│   ├─► File type hint            │
│   └─► Hidden file input         │
├─────────────────────────────────┤
│ File Preview (if selected)      │
│   ├─► Filename                  │
│   ├─► File size                 │
│   └─► Image preview             │
├─────────────────────────────────┤
│ Upload Button                   │
│   └─► Disabled until file       │
├─────────────────────────────────┤
│ View Gallery Button             │
└─────────────────────────────────┘

GALLERY PAGE COMPONENTS
┌─────────────────────────────────┐
│ Header                          │
│   ├─► Title: "📸 Photo Gallery" │
│   └─► Subtitle                  │
├─────────────────────────────────┤
│ Controls                        │
│   └─► Upload New Photo button   │
├─────────────────────────────────┤
│ Photo Count                     │
│   └─► "X photos in gallery"     │
├─────────────────────────────────┤
│ Photo Grid                      │
│   └─► Photo Cards               │
│       ├─► Image                 │
│       ├─► Filename              │
│       ├─► Date                  │
│       ├─► Size                  │
│       ├─► View Full button      │
│       └─► Delete button         │
├─────────────────────────────────┤
│ Modal (on image click)          │
│   ├─► Full screen overlay       │
│   ├─► Large image preview       │
│   └─► Close button (X)          │
└─────────────────────────────────┘
```

## 🚀 Deployment Pipeline

```
LOCAL → GITHUB → RENDER → PRODUCTION

1. LOCAL DEVELOPMENT
   └─► Code changes
          │
          ▼
2. GIT COMMIT
   └─► git add .
   └─► git commit -m "..."
          │
          ▼
3. PUSH TO GITHUB
   └─► git push origin main
          │
          ▼
4. RENDER DETECTS PUSH
   └─► Webhook triggered
          │
          ▼
5. BUILD PHASE
   ├─► Install Python 3.11
   ├─► pip install -r requirements.txt
   └─► Verify dependencies
          │
          ▼
6. DEPLOY PHASE
   ├─► Start gunicorn
   ├─► Health check
   └─► Route traffic
          │
          ▼
7. PRODUCTION LIVE
   └─► https://your-app.onrender.com
```

---

## 📋 Quick Reference

### Azure Operations
- Create: `storage.create_container()`
- Upload: `storage.upload_file(file, name)`
- List: `storage.list_files()`
- Delete: `storage.delete_file(name)`
- Check: `storage.file_exists(name)`

### Flask Routes
- `GET /` → Upload page
- `POST /upload` → Handle upload
- `GET /gallery` → Show gallery
- `POST /delete/<filename>` → Delete file
- `GET /health` → Health check

### Environment Variables
- `AZURE_STORAGE_CONNECTION_STRING` (required)
- `AZURE_CONTAINER_NAME` (default: photos)
- `SECRET_KEY` (Flask sessions)
- `PORT` (default: 5000)

---

**This visual guide provides a comprehensive overview of the system architecture, data flows, and user interactions.** 🎨
