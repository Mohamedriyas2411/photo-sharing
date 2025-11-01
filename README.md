# 📸 Photo Sharing Platform

A cloud-based photo sharing platform built with Python Flask and AWS S3, designed for secure file storage and retrieval. Deploy easily with AWS Amplify!

## ✨ Features

- **AWS S3 Storage**: Upload images securely to Amazon S3
- **Easy Deployment**: Deploy in minutes with AWS Amplify
- **File Operations**: Upload, view, and delete photos
- **Beautiful UI**: Modern, responsive interface with drag-and-drop support
- **Image Gallery**: Browse all uploaded photos with preview functionality
- **File Validation**: Support for PNG, JPG, JPEG, GIF, and WEBP formats
- **Size Management**: Maximum 16MB file size with automatic validation
- **Auto-Deploy**: Automatic deployments from GitHub

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Browser   │ ───> │ Flask App    │ ───> │   AWS S3        │
│  (Client)   │      │ (Amplify)    │      │   Bucket        │
└─────────────┘      └──────────────┘      └─────────────────┘
                           │
                           ├── app.py (Routes & Logic)
                           ├── aws_storage_service.py (AWS SDK)
                           └── templates/ (HTML UI)
```

## 📋 Prerequisites

- Python 3.11 or higher
- AWS Account (free tier available)
- Git and GitHub account
- Your code pushed to GitHub repository

## 🚀 AWS Amplify Deployment Guide

### Step 1: Create S3 Bucket for Photos

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/s3/)
2. Click **"Create bucket"**
3. **Bucket name**: Choose a unique name (e.g., `my-photo-app-2025`)
4. **Region**: Select closest to you (e.g., `us-east-1`)
5. **Uncheck** "Block all public access" ⚠️
6. Acknowledge the warning
7. Click **"Create bucket"**

8. **Set Bucket Policy** (Make images publicly readable):
   - Click your bucket name
   - Go to **"Permissions"** tab
   - Click **"Bucket Policy"**
   - Paste this (replace `YOUR-BUCKET-NAME`):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
       }
     ]
   }
   ```
   - Click **"Save changes"**

### Step 2: Get AWS Credentials

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **"Users"** → **"Create user"**
3. Username: `photo-app-user`
4. Click **"Next"**
5. Select **"Attach policies directly"**
6. Search and check: **"AmazonS3FullAccess"**
7. Click **"Next"** → **"Create user"**
8. Click on the new user → **"Security credentials"** tab
9. Click **"Create access key"**
10. Select **"Application running outside AWS"**
11. Click **"Next"** → **"Create access key"**
12. **⚠️ SAVE THESE** (you won't see them again):
    - Access key ID
    - Secret access key

### Step 3: Push Your Code to GitHub

```powershell
git add .
git commit -m "Ready for AWS Amplify deployment"
git push origin main
```

### Step 4: Deploy to AWS Amplify

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
2. Click **"New app"** → **"Host web app"**
3. Choose **"GitHub"** → Click **"Continue"**
4. Authorize AWS Amplify (if needed)
5. Select your repository: **"carRentaal"**
6. Branch: **"main"**
7. Click **"Next"**

### Step 5: Configure Build Settings

1. App name: `photo-sharing-app`
2. The build settings will use your `amplify.yml` file
3. Click **"Advanced settings"**
4. **Add environment variables**:
   ```
   STORAGE_TYPE = aws
   AWS_ACCESS_KEY_ID = your-access-key-from-step-2
   AWS_SECRET_ACCESS_KEY = your-secret-key-from-step-2
   AWS_S3_BUCKET = your-bucket-name-from-step-1
   AWS_REGION = us-east-1
   SECRET_KEY = any-random-string-here
   PORT = 8080
   ```
5. Click **"Next"** → **"Save and deploy"**

### Step 6: Wait for Deployment ⏳

- Deployment takes 5-10 minutes
- Watch the build logs for any errors
- Once complete, you'll get a URL like:
  ```
  https://main.d1a2b3c4d5e6f.amplifyapp.com
  ```

### Step 7: Test Your App! 🎉

1. Click the Amplify URL
2. Upload a photo
3. View it in the gallery
4. Check your S3 bucket - photos are there!

## 🔄 Automatic Updates

Every time you push to GitHub, Amplify automatically redeploys:
```powershell
git add .
git commit -m "Your changes"
git push origin main
```

## 💰 Cost Estimate

**AWS Free Tier includes:**
- S3: 5GB storage, 20,000 GET requests/month
- Amplify: 1,000 build minutes/month, 15GB served/month

**Typical cost after free tier:** $0-5/month for small apps

## 📦 Project Structure

```
photo sharing platform/
├── app.py                      # Flask application with routes
├── aws_storage_service.py      # AWS S3 storage service
├── local_storage_service.py    # Local storage (for dev)
├── storage_service.py          # Storage factory
├── requirements.txt            # Python dependencies
├── amplify.yml                 # AWS Amplify configuration
├── Procfile                    # Process configuration
├── .env                        # Environment variables (DO NOT COMMIT!)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── templates/
    ├── index.html              # Upload page
    └── gallery.html            # Gallery page
```

## � Troubleshooting

### Build Fails in Amplify
- Check build logs in Amplify console
- Verify `amplify.yml` file is present
- Check all dependencies in `requirements.txt`

### Images Don't Upload
- Verify S3 bucket policy allows public read
- Check AWS credentials in environment variables
- Ensure AWS region matches your bucket region

### App Won't Start
- Check logs in Amplify console under "Logs"
- Verify `PORT=8080` environment variable
- Make sure `Procfile` exists with correct content

### "Access Denied" Errors
- Check IAM user has `AmazonS3FullAccess` permission
- Verify access keys are correct in environment variables

### Images Upload but Don't Display
- Check S3 bucket policy - must allow public GetObject
- Verify bucket name in environment variables matches actual bucket

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use Amplify environment variables** - Store secrets securely
3. **Rotate AWS keys regularly** - Change access keys every 90 days
4. **Keep S3 bucket properly configured** - Only public read, not write
5. **Monitor AWS CloudTrail** - Track all API calls

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `STORAGE_TYPE` | Storage backend | `aws` |
| `AWS_ACCESS_KEY_ID` | AWS access key | From IAM user |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | From IAM user |
| `AWS_S3_BUCKET` | S3 bucket name | `my-photo-app-2025` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `SECRET_KEY` | Flask secret | Any random string |
| `PORT` | Application port | `8080` |

## 🧹 Clean Up (To Avoid Charges)

If you want to delete everything:

1. **Delete Amplify App**:
   - AWS Amplify Console → Your app → App settings → Delete app

2. **Delete S3 Bucket**:
   - S3 Console → Your bucket → Empty → Delete

3. **Delete IAM User**:
   - IAM Console → Users → photo-app-user → Delete

## 📚 Resources

- [AWS Amplify Documentation](https://docs.aws.amazon.com/amplify/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Boto3 (AWS SDK) Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

## � You're All Set!

Your photo sharing app is now deployed on AWS with:
- ✅ Scalable storage on S3
- ✅ Automatic deployments from GitHub
- ✅ HTTPS enabled by default
- ✅ Free tier eligible

**Questions?** Check the troubleshooting section above or AWS documentation.
