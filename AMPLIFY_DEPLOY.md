# 🚀 AWS Amplify Deployment - Quick Steps

## ✅ What I've Done For You

1. ✅ Removed all unnecessary .md documentation files
2. ✅ Created `amplify.yml` for AWS Amplify configuration
3. ✅ Created `Procfile` for process management
4. ✅ Updated `README.md` with Amplify deployment instructions
5. ✅ Updated `.env` with AWS configuration template
6. ✅ Pushed all changes to GitHub

---

## 📋 Your Deployment Checklist

### Step 1: Create S3 Bucket (5 minutes)
1. Go to: https://s3.console.aws.amazon.com/s3/
2. Click **"Create bucket"**
3. Name it something unique: `my-photo-app-2025` or similar
4. **Region**: Choose `us-east-1` (or closest to you)
5. **IMPORTANT**: Uncheck "Block all public access"
6. Click **"Create bucket"**

7. **Set Bucket Policy**:
   - Click your bucket → **Permissions** tab → **Bucket Policy**
   - Paste this (replace YOUR-BUCKET-NAME):
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

### Step 2: Create IAM User (5 minutes)
1. Go to: https://console.aws.amazon.com/iam/
2. Click **Users** → **Create user**
3. Username: `photo-app-user`
4. Click **Next**
5. Select **"Attach policies directly"**
6. Search and check: **"AmazonS3FullAccess"**
7. Click **Next** → **Create user**
8. Click on user → **Security credentials** → **Create access key**
9. Choose **"Application running outside AWS"**
10. **SAVE THESE** (you won't see them again!):
    - Access Key ID
    - Secret Access Key

### Step 3: Deploy to AWS Amplify (10 minutes)
1. Go to: https://console.aws.amazon.com/amplify/
2. Click **"New app"** → **"Host web app"**
3. Choose **GitHub** → Authorize if needed
4. Select:
   - Repository: **carRentaal**
   - Branch: **main**
5. Click **Next**
6. App name: `photo-sharing-app`
7. Click **"Advanced settings"**

8. **Add these environment variables**:
   ```
   STORAGE_TYPE = aws
   AWS_ACCESS_KEY_ID = [paste your access key from Step 2]
   AWS_SECRET_ACCESS_KEY = [paste your secret key from Step 2]
   AWS_S3_BUCKET = [your bucket name from Step 1]
   AWS_REGION = us-east-1
   SECRET_KEY = random-string-here-123456
   PORT = 8080
   ```

9. Click **Next** → **Save and deploy**

### Step 4: Wait & Test (10 minutes)
- Watch the build progress
- Once done, you'll get a URL like: `https://main.d123abc456.amplifyapp.com`
- Click it and test uploading a photo!

---

## 🎯 Quick Test Checklist
- [ ] Can access the Amplify URL
- [ ] Can upload a photo
- [ ] Photo appears in gallery
- [ ] Photo is stored in S3 bucket
- [ ] Can delete photo

---

## 🔄 Future Updates
Whenever you make changes:
```powershell
git add .
git commit -m "Your changes"
git push origin main
```
Amplify automatically redeploys! ✨

---

## 💰 Cost
- **Free Tier**: 5GB S3 storage, 1000 build minutes
- **After**: Usually $0-5/month for small apps

---

## 📧 Environment Variables You Need

Copy these to Amplify (fill in your values):
```
STORAGE_TYPE=aws
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJalr...
AWS_S3_BUCKET=my-photo-app-2025
AWS_REGION=us-east-1
SECRET_KEY=random-secret-key-12345
PORT=8080
```

---

## 🐛 Common Issues

**Build fails?**
- Check Amplify build logs
- Verify all environment variables are set

**Photos don't upload?**
- Check S3 bucket policy
- Verify IAM user has S3FullAccess

**Photos upload but don't show?**
- Check bucket policy allows public GetObject
- Verify bucket name matches environment variable

---

## 🎉 That's It!

Your app should now be live on AWS Amplify with S3 storage!

**Your App URLs:**
- Live App: [Will be provided by Amplify]
- S3 Bucket: https://s3.console.aws.amazon.com/s3/buckets/[your-bucket-name]

---

**Need help?** Check the full README.md or AWS documentation.
