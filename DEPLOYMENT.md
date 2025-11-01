# 🚀 Deployment Guide - Render.com

Complete step-by-step guide to deploy your Photo Sharing Platform on Render.com

## 📋 Prerequisites

- [x] GitHub account
- [x] Render.com account (free tier available)
- [x] Azure Storage Account with connection string
- [x] Git installed on your computer

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

Open PowerShell in your project directory:

```powershell
cd "c:\Users\moham\Desktop\photo sharing platform"
git init
```

### 1.2 Create .gitignore (Already Done)

The `.gitignore` file ensures sensitive data doesn't get committed.

### 1.3 Add Files and Commit

```powershell
git add .
git commit -m "Initial commit: Photo sharing platform with Azure Blob Storage"
```

### 1.4 Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" icon → "New repository"
3. Name: `photo-sharing-platform` (or your choice)
4. Description: "Cloud-based photo sharing platform with Flask and Azure Blob Storage"
5. Keep it Public or Private (your choice)
6. **Do NOT** initialize with README (we already have one)
7. Click "Create repository"

### 1.5 Push to GitHub

GitHub will show commands like this - run them:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/photo-sharing-platform.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 🌐 Step 2: Deploy on Render

### 2.1 Sign Up / Log In to Render

1. Go to [Render.com](https://render.com)
2. Click "Get Started" or "Sign In"
3. Sign in with GitHub (recommended)
4. Authorize Render to access your repositories

### 2.2 Create New Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect a repository"** (or "+ New Web Service")
4. Find your `photo-sharing-platform` repository
5. Click **"Connect"**

### 2.3 Configure Service

Render will auto-detect settings from `render.yaml`, but verify:

**Basic Settings:**
- **Name**: `photo-sharing-platform` (or your choice)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: (leave empty)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add the following variables:

| Key | Value | Notes |
|-----|-------|-------|
| `AZURE_STORAGE_CONNECTION_STRING` | Your connection string from Azure | Required |
| `AZURE_CONTAINER_NAME` | `photos` | Optional (default: photos) |
| `SECRET_KEY` | (auto-generated) | Render generates this |
| `PYTHON_VERSION` | `3.11.0` | Optional |

**Getting your Azure connection string:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Storage Account
3. Go to "Security + networking" → "Access keys"
4. Copy "Connection string" from key1 or key2
5. Paste into Render

### 2.5 Select Plan

- **Free Plan**: 
  - ✓ Good for testing and demo
  - ✓ 750 hours/month free
  - ⚠ Spins down after 15 min inactivity
  - ⚠ First request after spin-down takes ~30 seconds
  
- **Starter Plan** ($7/month):
  - ✓ Always on (no spin-down)
  - ✓ Faster performance
  - ✓ Better for production

Choose **Free** for now.

### 2.6 Deploy

1. Review all settings
2. Click **"Create Web Service"**
3. Render will start building your app

**Build Process:**
- Installing dependencies
- Setting up Python environment
- Running build command
- Starting application

This takes about 2-3 minutes.

## ✅ Step 3: Verify Deployment

### 3.1 Check Build Logs

Watch the logs during deployment. You should see:
```
==> Installing dependencies from requirements.txt
==> Successfully installed Flask-3.0.0 azure-storage-blob-12.19.0 ...
==> Build successful!
==> Starting service with 'gunicorn app:app'
```

### 3.2 Access Your Application

Once deployed, Render provides a URL:
```
https://photo-sharing-platform-xxxx.onrender.com
```

Click on it or copy it to your browser.

### 3.3 Test All Features

1. **Home Page**: Should load with upload form
2. **Health Check**: Visit `/health` endpoint
   - Should return: `{"status": "healthy", "storage_configured": true}`
3. **Upload Photo**: Try uploading an image
4. **View Gallery**: Click "View Gallery" to see uploaded photos
5. **Delete Photo**: Test delete functionality

## 🔍 Step 4: Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Fix**: Ensure `requirements.txt` is correct and committed

**Error**: `Python version not supported`
- **Fix**: Add `PYTHON_VERSION=3.11.0` environment variable

### App Crashes on Start

**Error**: `Azure Storage initialization failed`
- **Fix**: Check `AZURE_STORAGE_CONNECTION_STRING` is set correctly

**Error**: `bind: address already in use`
- **Fix**: Remove hardcoded port from `app.py`, let Render set it

### Upload Fails

**Error**: `Storage service not configured`
- **Fix**: Verify environment variables are set in Render

**Error**: `Authentication failed`
- **Fix**: Check your Azure connection string is valid

### Slow First Request

**Behavior**: First request takes 30+ seconds
- **Reason**: Free tier spins down after inactivity
- **Fix**: Upgrade to Starter plan or use a keep-alive service

## 🎨 Step 5: Custom Domain (Optional)

### 5.1 Add Custom Domain

1. In Render Dashboard, go to your service
2. Click **"Settings"**
3. Scroll to **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter your domain (e.g., `photos.yourdomain.com`)
6. Add the provided CNAME record to your DNS provider

### 5.2 SSL Certificate

Render automatically provisions and renews SSL certificates for free!

## 📊 Step 6: Monitor Your App

### View Logs

- Click **"Logs"** tab in Render dashboard
- See real-time application logs
- Monitor errors and requests

### Metrics

- Click **"Metrics"** tab
- View CPU, memory, bandwidth usage
- Check request counts and response times

### Health Checks

Render automatically monitors `/health` endpoint and restarts if needed.

## 🔄 Step 7: Update Your App

### Make Changes Locally

```powershell
# Make your changes
# Edit files...

# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main
```

**Automatic Deployment:**
- Render detects the push
- Automatically rebuilds and redeploys
- Zero downtime deployment

## 🛡️ Security Best Practices

### Environment Variables
- ✓ Never commit `.env` file
- ✓ Use environment variables for all secrets
- ✓ Rotate Azure keys periodically

### Azure Storage
- ✓ Use dedicated storage account for this app
- ✓ Monitor access logs
- ✓ Set up lifecycle policies to manage old files

### Application
- ✓ Keep dependencies updated
- ✓ Monitor error logs
- ✓ Set file size limits (already at 16MB)

## 💰 Cost Breakdown

### Azure Storage (Blob Storage)
- **Storage**: ~$0.02/GB/month (Hot tier)
- **Operations**: ~$0.05 per 10,000 operations
- **Example**: 1GB of photos + 1000 uploads/month = ~$0.07/month

### Render
- **Free Plan**: $0 (750 hours/month)
- **Starter Plan**: $7/month (always-on)

**Total Monthly Cost**: ~$0-7 (excluding Azure, which is pennies)

## 📱 Step 8: Share Your App

Your app is now live! Share the URL:
```
https://your-app-name.onrender.com
```

Features available:
- ✓ Upload photos from any device
- ✓ View photo gallery
- ✓ Delete photos
- ✓ Responsive design (works on mobile)
- ✓ Secure HTTPS connection
- ✓ Cloud storage with Azure

## 🚀 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Environment variables configured
- [ ] Build successful
- [ ] App is accessible
- [ ] Health check passes
- [ ] Upload test successful
- [ ] Gallery working
- [ ] Delete function working

## 🎓 Learning Achievements

You've successfully:
- ✅ Built a Flask web application
- ✅ Integrated Azure Blob Storage
- ✅ Implemented container creation
- ✅ Created file upload/download functionality
- ✅ Deployed to cloud (Render)
- ✅ Configured environment variables
- ✅ Set up continuous deployment

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure Blob Storage Docs](https://docs.microsoft.com/azure/storage/blobs/)
- [GitHub Guides](https://guides.github.com/)

## 💡 Next Steps

1. **Add Features**: User auth, private albums, image editing
2. **Optimize**: Add caching, image compression
3. **Monitor**: Set up alerts and monitoring
4. **Scale**: Upgrade plan as usage grows

---

**Congratulations! Your photo sharing platform is live! 🎉**
