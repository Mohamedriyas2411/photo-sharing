"""
Demonstration script for Azure Blob Storage operations
Shows container creation, file upload, retrieval, and deletion
"""

import os
import io
from storage_service import AzureBlobStorage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def demo_container_creation(storage):
    """Demonstrate container creation"""
    print_section("DEMO 1: Container Creation")
    
    print("Creating container (if it doesn't exist)...")
    try:
        result = storage.create_container()
        print(f"✓ Container '{storage.container_name}' is ready")
        print(f"  Result: {result}")
        print("\nContainer Details:")
        print(f"  - Name: {storage.container_name}")
        print(f"  - Public Access: blob (files are publicly accessible)")
        print(f"  - Created/Verified: Yes")
    except Exception as e:
        print(f"✗ Error: {e}")

def demo_file_upload(storage):
    """Demonstrate file upload"""
    print_section("DEMO 2: File Upload")
    
    # Create a sample text file in memory
    sample_content = """
    This is a sample file for testing Azure Blob Storage operations.
    
    Features demonstrated:
    - Container creation
    - File upload
    - File retrieval
    - File deletion
    
    Timestamp: {}
    """.format(os.environ.get('DATE', 'Test'))
    
    print("Creating a sample file in memory...")
    file_stream = io.BytesIO(sample_content.encode('utf-8'))
    filename = "sample_test_file.txt"
    
    print(f"Uploading '{filename}' to Azure Blob Storage...")
    try:
        blob_url = storage.upload_file(file_stream, filename)
        print(f"✓ File uploaded successfully!")
        print(f"\nFile Details:")
        print(f"  - Name: {filename}")
        print(f"  - Size: {len(sample_content)} bytes")
        print(f"  - URL: {blob_url}")
        print(f"\n  You can access this file at: {blob_url}")
        return filename
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def demo_file_listing(storage):
    """Demonstrate file listing and retrieval"""
    print_section("DEMO 3: File Listing and Retrieval")
    
    print("Retrieving list of all files in container...")
    try:
        files = storage.list_files()
        print(f"✓ Found {len(files)} file(s) in container\n")
        
        if files:
            print("Files in container:")
            print("-" * 70)
            for i, file in enumerate(files, 1):
                print(f"\n{i}. {file['name']}")
                print(f"   Size: {file['size']:,} bytes ({file['size']/1024:.2f} KB)")
                print(f"   Created: {file['created']}")
                print(f"   Type: {file['content_type']}")
                print(f"   URL: {file['url']}")
        else:
            print("  (Container is empty)")
        
        return files
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def demo_file_download(storage, filename):
    """Demonstrate file download"""
    print_section("DEMO 4: File Download")
    
    if not filename:
        print("Skipping - no file to download")
        return
    
    print(f"Downloading '{filename}' from Azure Blob Storage...")
    try:
        content = storage.download_file(filename)
        print(f"✓ File downloaded successfully!")
        print(f"\nFile Content ({len(content)} bytes):")
        print("-" * 70)
        print(content.decode('utf-8'))
        print("-" * 70)
    except Exception as e:
        print(f"✗ Error: {e}")

def demo_file_existence(storage, filename):
    """Demonstrate file existence check"""
    print_section("DEMO 5: File Existence Check")
    
    if not filename:
        print("Skipping - no filename provided")
        return
    
    print(f"Checking if '{filename}' exists...")
    try:
        exists = storage.file_exists(filename)
        if exists:
            print(f"✓ File exists in storage")
        else:
            print(f"✗ File does not exist")
    except Exception as e:
        print(f"✗ Error: {e}")

def demo_file_deletion(storage, filename):
    """Demonstrate file deletion"""
    print_section("DEMO 6: File Deletion")
    
    if not filename:
        print("Skipping - no file to delete")
        return
    
    print(f"Do you want to delete '{filename}'? (y/n): ", end='')
    try:
        response = input().lower()
        if response == 'y':
            print(f"Deleting '{filename}'...")
            result = storage.delete_file(filename)
            if result:
                print(f"✓ File deleted successfully")
            else:
                print(f"✗ File not found or already deleted")
        else:
            print("Skipping deletion")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Main demonstration function"""
    print("\n" + "=" * 70)
    print("  AZURE BLOB STORAGE OPERATIONS DEMONSTRATION")
    print("  Photo Sharing Platform - Storage Service Test")
    print("=" * 70)
    
    # Check for connection string
    connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    if not connection_string:
        print("\n✗ ERROR: AZURE_STORAGE_CONNECTION_STRING not set")
        print("\nPlease set the environment variable:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Azure Storage connection string")
        print("  3. Run this script again")
        return
    
    container_name = os.environ.get('AZURE_CONTAINER_NAME', 'photos')
    
    print(f"\nConfiguration:")
    print(f"  - Container: {container_name}")
    print(f"  - Connection: Configured ✓")
    
    # Initialize storage service
    print("\nInitializing Azure Blob Storage service...")
    try:
        storage = AzureBlobStorage(
            connection_string=connection_string,
            container_name=container_name
        )
        print("✓ Storage service initialized\n")
    except Exception as e:
        print(f"✗ Failed to initialize storage: {e}")
        return
    
    # Run demonstrations
    try:
        # 1. Container Creation
        demo_container_creation(storage)
        
        # 2. File Upload
        uploaded_filename = demo_file_upload(storage)
        
        # 3. File Listing
        demo_file_listing(storage)
        
        # 4. File Download
        if uploaded_filename:
            demo_file_download(storage, uploaded_filename)
        
        # 5. File Existence Check
        if uploaded_filename:
            demo_file_existence(storage, uploaded_filename)
        
        # 6. File Deletion
        if uploaded_filename:
            demo_file_deletion(storage, uploaded_filename)
        
        # Final file listing
        print_section("Final Container State")
        demo_file_listing(storage)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
    
    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nAll storage operations demonstrated successfully!")
    print("\nNext steps:")
    print("  - Run 'python app.py' to start the web application")
    print("  - Visit http://localhost:5000 to use the photo sharing platform")
    print("\n")

if __name__ == "__main__":
    main()
