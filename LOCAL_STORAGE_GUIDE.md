# 💾 Local Storage Setup Guide

## Overview

The application now supports **two storage options**:

1. **Local Storage** (System) - Files stored on your computer/server
2. **Azure Blob Storage** (Cloud) - Files stored in Azure cloud

## 🚀 Quick Start with Local Storage

### 1️⃣ Configure Storage Type

Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:
```env
STORAGE_TYPE=local
```

That's it! No Azure account needed.

### 2️⃣ Run the Application

```powershell
python app.py
```

Files will be stored in: `uploads/photos/`

## 📊 Storage Comparison

| Feature | Local Storage | Azure Blob Storage |
|---------|--------------|-------------------|
| **Cost** | Free | ~$0.02/GB/month |
| **Setup** | Instant | Requires Azure account |
| **Configuration** | Just set `STORAGE_TYPE=local` | Need connection string |
| **Access Speed** | Very fast (local disk) | Fast (network) |
| **Scalability** | Limited by disk space | Unlimited |
| **Durability** | Single machine | Cloud redundancy |
| **Backup** | Manual | Automatic |
| **Best For** | Development, small projects | Production, large scale |

## 🔧 Configuration Options

### Option 1: Local Storage (System)

**File: `.env`**
```env
STORAGE_TYPE=local
```

**Storage Location:**
- Windows: `C:\Users\...\photo sharing platform\uploads\photos\`
- Linux/Mac: `~/photo-sharing-platform/uploads/photos/`

**Advantages:**
- ✅ No cloud account needed
- ✅ Free forever
- ✅ Very fast (local disk)
- ✅ Works offline
- ✅ Full control

**Limitations:**
- ⚠ Limited by disk space
- ⚠ Files lost if disk fails
- ⚠ Not accessible from other machines
- ⚠ Manual backup needed

### Option 2: Azure Blob Storage (Cloud)

**File: `.env`**
```env
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
AZURE_CONTAINER_NAME=photos
```

**Storage Location:**
- Azure Data Center (global CDN)

**Advantages:**
- ✅ Unlimited storage
- ✅ Cloud redundancy
- ✅ Accessible globally
- ✅ Automatic backups
- ✅ CDN integration

**Limitations:**
- ⚠ Requires Azure account
- ⚠ Small cost (~$0.02/GB/month)
- ⚠ Internet required
- ⚠ Slightly slower (network latency)

## 🏃 Quick Test

### Test Local Storage

```powershell
# 1. Set to local storage
# Edit .env: STORAGE_TYPE=local

# 2. Run the app
python app.py

# 3. Upload a photo
# Open http://localhost:5000

# 4. Check uploads folder
dir uploads\photos
```

### Test Azure Storage

```powershell
# 1. Set to Azure storage
# Edit .env: STORAGE_TYPE=azure
# Add: AZURE_STORAGE_CONNECTION_STRING=...

# 2. Run the app
python app.py

# 3. Upload a photo
# Open http://localhost:5000

# 4. Check Azure Portal
# Storage Account -> Containers -> photos
```

## 🔀 Switching Between Storage Types

You can switch at any time by changing `STORAGE_TYPE` in `.env`:

### Switch to Local
```env
STORAGE_TYPE=local
```

### Switch to Azure
```env
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

**Note:** Files uploaded to one storage type won't appear when you switch. They're stored in different locations.

## 📂 File Storage Locations

### Local Storage
```
photo sharing platform/
└── uploads/
    └── photos/
        ├── photo1.jpg
        ├── photo2.png
        └── photo3.gif
```

### Azure Storage
```
Azure Storage Account
└── Container: photos
    ├── photo1.jpg
    ├── photo2.png
    └── photo3.gif
```

## 🛠️ Advanced Configuration

### Change Local Storage Path

Edit `app.py`:
```python
storage = LocalFileStorage(
    storage_path='my_custom_path',  # Change this
    container_name='photos'
)
```

### Multiple Containers

Local:
```python
storage = LocalFileStorage(
    storage_path='uploads',
    container_name='photos'  # or 'videos', 'documents', etc.
)
```

Azure:
```env
AZURE_CONTAINER_NAME=my-custom-container
```

## 🚀 Deployment Options

### Local Deployment (Render with Local Storage)

**Not Recommended** - Render's filesystem is ephemeral (files deleted on restart)

### Cloud Deployment (Render with Azure Storage)

**Recommended** - Files persist across restarts

In Render environment variables:
```
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

### Self-Hosted (Your Server with Local Storage)

**Works Great** - Full control, persistent storage

## 💡 Use Cases

### Local Storage Best For:
- 🏠 Personal use
- 💻 Development/testing
- 🎓 Learning projects
- 🔒 Private/sensitive data
- 📴 Offline applications

### Azure Storage Best For:
- 🌐 Production websites
- 📈 Scalable applications
- 👥 Multi-user platforms
- 🌍 Global access
- 💼 Business applications

## 🔐 Security Considerations

### Local Storage
- Files accessible via file system
- Protected by OS permissions
- Backup manually
- Use firewall for network access

### Azure Storage
- Files publicly accessible via URL
- Protected by Azure security
- Automatic backups
- Can configure private access

## 📊 Performance Tips

### Local Storage
```python
# Faster for small files
# Lower latency
# No network overhead
```

### Azure Storage
```python
# Better for large files
# CDN acceleration
# Global distribution
```

## 🐛 Troubleshooting

### "Permission denied" (Local Storage)
➜ Check folder permissions
➜ Run as administrator (Windows)

### "Directory not found" (Local Storage)
➜ App creates it automatically
➜ Check file path in app.py

### "Azure connection failed"
➜ Check connection string
➜ Verify Azure account active

### Files disappear after restart (Render)
➜ Switch to Azure storage
➜ Render's local storage is temporary

## 🔄 Migration Between Storage Types

### From Local to Azure

1. Upload files manually to Azure:
```python
from storage_service import AzureBlobStorage
from local_storage_service import LocalFileStorage

local = LocalFileStorage('uploads', 'photos')
azure = AzureBlobStorage(connection_string, 'photos')

# Copy files
for file in local.list_files():
    content = local.download_file(file['name'])
    azure.upload_file(content, file['name'])
```

2. Update `.env`:
```env
STORAGE_TYPE=azure
```

### From Azure to Local

1. Download files:
```python
azure = AzureBlobStorage(connection_string, 'photos')
local = LocalFileStorage('uploads', 'photos')

# Copy files
for file in azure.list_files():
    content = azure.download_file(file['name'])
    local.upload_file(content, file['name'])
```

2. Update `.env`:
```env
STORAGE_TYPE=local
```

## ✅ Quick Decision Guide

**Choose Local Storage if:**
- ✅ Just learning/testing
- ✅ Running on your own server
- ✅ Want zero cost
- ✅ Small project (< 100 photos)
- ✅ Single user

**Choose Azure Storage if:**
- ✅ Deploying to Render/Heroku
- ✅ Multiple users
- ✅ Need reliability
- ✅ Large scale (1000+ photos)
- ✅ Production application

## 🎯 Recommendations

### Development: Local Storage
```env
STORAGE_TYPE=local
```
Fast, free, simple.

### Production: Azure Storage
```env
STORAGE_TYPE=azure
AZURE_STORAGE_CONNECTION_STRING=...
```
Reliable, scalable, persistent.

---

## 📝 Summary

- **Set `STORAGE_TYPE=local`** → Files on your computer
- **Set `STORAGE_TYPE=azure`** → Files in cloud
- **Switch anytime** by changing .env
- **Local = Free & Fast**, Azure = Reliable & Scalable

**Default is Local Storage** - just run `python app.py`!

---

**Need help?** Check the main README.md or run `python setup.py`
