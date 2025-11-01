"""
Test AWS S3 Storage Configuration
Verifies AWS credentials and S3 bucket setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aws_configuration():
    """Test AWS S3 storage configuration"""
    
    print("=" * 60)
    print("AWS S3 STORAGE CONFIGURATION TEST")
    print("=" * 60)
    print()
    
    # Check environment variables
    print("📋 Checking Environment Variables...")
    print("-" * 60)
    
    storage_type = os.environ.get('STORAGE_TYPE', 'not set')
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID', 'not set')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', 'not set')
    aws_region = os.environ.get('AWS_REGION', 'not set')
    aws_bucket = os.environ.get('AWS_BUCKET_NAME', 'not set')
    
    print(f"STORAGE_TYPE: {storage_type}")
    print(f"AWS_ACCESS_KEY_ID: {'✓ Set' if aws_access_key != 'not set' else '✗ Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'✓ Set' if aws_secret_key != 'not set' else '✗ Not set'}")
    print(f"AWS_REGION: {aws_region}")
    print(f"AWS_BUCKET_NAME: {aws_bucket}")
    print()
    
    if storage_type.lower() != 'aws':
        print("⚠️  STORAGE_TYPE is not set to 'aws'")
        print("   Update your .env file: STORAGE_TYPE=aws")
        print()
    
    if aws_access_key == 'not set' or aws_secret_key == 'not set':
        print("❌ AWS credentials not configured!")
        print()
        print("To fix this:")
        print("1. Create IAM user in AWS Console")
        print("2. Download credentials CSV")
        print("3. Update .env file with:")
        print("   AWS_ACCESS_KEY_ID=your_access_key")
        print("   AWS_SECRET_ACCESS_KEY=your_secret_key")
        print()
        return False
    
    if aws_bucket == 'not set':
        print("❌ AWS_BUCKET_NAME not configured!")
        print()
        print("To fix this:")
        print("1. Create S3 bucket in AWS Console")
        print("2. Update .env file: AWS_BUCKET_NAME=your-bucket-name")
        print()
        return False
    
    # Try to import boto3
    print("📦 Checking Dependencies...")
    print("-" * 60)
    
    try:
        import boto3
        print("✓ boto3 installed")
    except ImportError:
        print("❌ boto3 not installed!")
        print()
        print("To fix this:")
        print("  pip install boto3")
        print()
        return False
    
    print()
    
    # Try to initialize S3 storage
    print("🔧 Testing AWS S3 Connection...")
    print("-" * 60)
    
    try:
        from aws_storage_service import AWSS3Storage
        
        storage = AWSS3Storage(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
            bucket_name=aws_bucket
        )
        
        print("✓ AWS S3 client initialized successfully")
        print()
        
        # Try to create/verify bucket
        print("📦 Verifying S3 Bucket...")
        print("-" * 60)
        
        try:
            storage.create_container()
            print(f"✓ Bucket '{aws_bucket}' is ready")
            print()
            
            # Try to list files
            print("📂 Listing files in bucket...")
            print("-" * 60)
            
            files = storage.list_files()
            
            if files:
                print(f"✓ Found {len(files)} file(s) in bucket:")
                for file in files[:5]:  # Show first 5
                    print(f"  - {file['name']} ({file['size']} bytes)")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more")
            else:
                print("✓ Bucket is empty (ready for uploads)")
            
            print()
            
        except Exception as e:
            print(f"❌ Error with bucket: {e}")
            print()
            print("Common issues:")
            print("1. Bucket doesn't exist - create it in AWS Console")
            print("2. Bucket name is wrong - check AWS_BUCKET_NAME in .env")
            print("3. Bucket is in different region - check AWS_REGION")
            print("4. IAM user lacks S3 permissions")
            print()
            return False
        
    except Exception as e:
        print(f"❌ Error initializing S3: {e}")
        print()
        print("Common issues:")
        print("1. Invalid credentials - check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("2. IAM user doesn't have S3 permissions")
        print("3. Network/firewall blocking AWS connection")
        print()
        return False
    
    # Success!
    print("=" * 60)
    print("✅ AWS S3 STORAGE CONFIGURED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run the Flask app: python app.py")
    print("2. Upload a test image")
    print("3. Check your S3 bucket in AWS Console")
    print()
    print("To deploy to AWS Elastic Beanstalk:")
    print("  See AWS_QUICKSTART.md for deployment guide")
    print()
    
    return True


def main():
    """Main function"""
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print()
        print("To create .env file:")
        print("1. Copy .env.example to .env")
        print("2. Update with your AWS credentials")
        print()
        sys.exit(1)
    
    success = test_aws_configuration()
    
    if not success:
        print("⚠️  Configuration test failed. Please fix the issues above.")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
