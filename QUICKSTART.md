# 🚀 Quick Start Guide

## Step-by-Step Setup (5 minutes)

### 1. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Get Azure Storage Connection String

**Option A: Create New Azure Storage Account**
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Storage account"
3. Fill in:
   - Resource group: Create new or select existing
   - Storage account name: Choose unique name (e.g., `photosharingstore123`)
   - Region: Select closest to you
   - Performance: Standard
   - Redundancy: LRS (cheapest option)
4. Click "Review + create" → "Create"
5. After deployment, go to your storage account
6. Navigate to "Security + networking" → "Access keys"
7. Copy "Connection string" from key1

**Option B: Use Existing Storage Account**
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Storage Account
3. Go to "Security + networking" → "Access keys"
4. Copy "Connection string"

### 3. Configure Environment
```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env with your connection string
notepad .env
```

Replace `your_azure_storage_connection_string_here` with your actual connection string.

### 4. Test Setup
```powershell
python setup.py
```

This will:
- ✓ Check environment variables
- ✓ Test Azure connection
- ✓ Create container automatically
- ✓ List existing files

### 5. Run Application
```powershell
python app.py
```

Open browser: http://localhost:5000

## 🎯 Deploy to Render.com

### 1. Create GitHub Repository
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/photo-sharing-platform.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Settings will auto-populate from `render.yaml`
5. Add environment variable:
   - Key: `AZURE_STORAGE_CONNECTION_STRING`
   - Value: Your connection string
6. Click "Create Web Service"

### 3. Access Your App
Your app will be live at: `https://your-app-name.onrender.com`

## 💡 Tips

- **Free Tier**: Render free tier spins down after inactivity (first request takes ~30 seconds)
- **Container**: The app automatically creates the "photos" container
- **Security**: Never commit `.env` file to Git
- **Storage Cost**: Azure Blob Storage is very cheap (~$0.02/GB/month)

## 🔍 Verify Everything Works

1. **Upload Test**: Upload an image on home page
2. **Gallery Test**: Click "View Gallery" to see uploaded images
3. **Delete Test**: Click "Delete" button on an image
4. **Health Check**: Visit `/health` endpoint

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `storage_service.py` for Azure operations
- See `app.py` for Flask routes

## ✅ Checklist

- [ ] Python 3.11+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Azure Storage Account created
- [ ] Connection string added to `.env`
- [ ] Setup test passed (`python setup.py`)
- [ ] App running locally (`python app.py`)
- [ ] GitHub repository created (for deployment)
- [ ] Deployed to Render.com

---

**Ready to go!** 🎉
