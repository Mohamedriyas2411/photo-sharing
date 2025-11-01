"""
AWS S3 Storage Service for Photo Sharing Platform
Handles bucket creation, file upload, retrieval, and deletion
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from typing import List, Dict
import mimetypes
from datetime import datetime

class AWSS3Storage:
    """
    AWS S3 Storage service for managing photo uploads
    """
    
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None, 
                 region_name: str = 'us-east-1', bucket_name: str = 'photos'):
        """
        Initialize AWS S3 Storage client
        
        Args:
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region_name: AWS region (default: us-east-1)
            bucket_name: Name of the S3 bucket to store photos
        """
        self.bucket_name = bucket_name
        self.region_name = region_name
        
        # Initialize S3 client
        try:
            if aws_access_key_id and aws_secret_access_key:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                )
            else:
                # Use IAM role or environment credentials
                self.s3_client = boto3.client('s3', region_name=region_name)
            
            print(f"✓ AWS S3 client initialized for region: {region_name}")
        except NoCredentialsError:
            print("✗ AWS credentials not found")
            raise
        except Exception as e:
            print(f"✗ Error initializing S3 client: {e}")
            raise
    
    def create_container(self) -> bool:
        """
        Create an S3 bucket if it doesn't exist
        
        Returns:
            True if bucket was created or already exists
        """
        try:
            # Check if bucket exists
            try:
                self.s3_client.head_bucket(Bucket=self.bucket_name)
                print(f"Bucket '{self.bucket_name}' already exists")
                return True
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    # Bucket doesn't exist, create it
                    if self.region_name == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region_name}
                        )
                    
                    # Set bucket policy for public read access (for images)
                    bucket_policy = {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "PublicReadGetObject",
                                "Effect": "Allow",
                                "Principal": "*",
                                "Action": "s3:GetObject",
                                "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                            }
                        ]
                    }
                    
                    import json
                    self.s3_client.put_bucket_policy(
                        Bucket=self.bucket_name,
                        Policy=json.dumps(bucket_policy)
                    )
                    
                    # Block public ACLs but allow bucket policy
                    self.s3_client.put_public_access_block(
                        Bucket=self.bucket_name,
                        PublicAccessBlockConfiguration={
                            'BlockPublicAcls': True,
                            'IgnorePublicAcls': True,
                            'BlockPublicPolicy': False,
                            'RestrictPublicBuckets': False
                        }
                    )
                    
                    print(f"Bucket '{self.bucket_name}' created successfully")
                    return True
                else:
                    raise
        except Exception as e:
            print(f"Error with bucket: {e}")
            raise
    
    def upload_file(self, file_stream, filename: str) -> str:
        """
        Upload a file to S3
        
        Args:
            file_stream: File object or stream to upload
            filename: Name of the file
            
        Returns:
            URL of the uploaded file
        """
        try:
            # Determine content type
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Reset file pointer to beginning
            if hasattr(file_stream, 'seek'):
                file_stream.seek(0)
            
            # Upload the file
            self.s3_client.upload_fileobj(
                file_stream,
                self.bucket_name,
                filename,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'max-age=31536000'
                }
            )
            
            # Generate URL
            file_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{filename}"
            print(f"File '{filename}' uploaded successfully")
            return file_url
            
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise
    
    def download_file(self, filename: str) -> bytes:
        """
        Download a file from S3
        
        Args:
            filename: Name of the file to download
            
        Returns:
            File content as bytes
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"File '{filename}' not found")
            raise
        except Exception as e:
            print(f"Error downloading file: {e}")
            raise
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from S3
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if file was deleted successfully
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            print(f"File '{filename}' deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            raise
    
    def list_files(self) -> List[Dict[str, str]]:
        """
        List all files in the bucket
        
        Returns:
            List of dictionaries containing file information
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            
            file_list = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    file_url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{obj['Key']}"
                    file_info = {
                        'name': obj['Key'],
                        'url': file_url,
                        'size': obj['Size'],
                        'created': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                        'content_type': 'image/*'
                    }
                    file_list.append(file_info)
            
            return file_list
            
        except Exception as e:
            print(f"Error listing files: {e}")
            raise
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists in the bucket
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError:
            return False
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False
    
    def get_file_url(self, filename: str) -> str:
        """
        Get the public URL for a file
        
        Args:
            filename: Name of the file
            
        Returns:
            Public URL for the file
        """
        return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{filename}"


# Example usage and testing
if __name__ == "__main__":
    """
    Test the AWS S3 Storage service
    """
    import sys
    
    # Get credentials from environment
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_REGION', 'us-east-1')
    bucket = os.environ.get('AWS_BUCKET_NAME', 'photos')
    
    if not aws_access_key or not aws_secret_key:
        print("Error: AWS credentials not set")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        sys.exit(1)
    
    # Initialize storage service
    storage = AWSS3Storage(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region,
        bucket_name=bucket
    )
    
    # Create bucket
    print("\n=== Creating Bucket ===")
    storage.create_container()
    
    # List files
    print("\n=== Listing Files ===")
    files = storage.list_files()
    if files:
        for file in files:
            print(f"- {file['name']} ({file['size']} bytes) - {file['created']}")
    else:
        print("No files in bucket")
    
    print("\n=== Storage Service Test Complete ===")
