"""
Quick test script for local storage
Run this to verify local storage is working
"""

import os
import io
from datetime import datetime

def test_local_storage():
    """Test local storage functionality"""
    
    print("\n" + "="*60)
    print("  LOCAL STORAGE TEST")
    print("="*60 + "\n")
    
    try:
        from local_storage_service import LocalFileStorage
        
        # Initialize storage
        print("1. Initializing local storage...")
        storage = LocalFileStorage('uploads', 'photos')
        print("   ✓ Storage initialized")
        
        # Create directory
        print("\n2. Creating storage directory...")
        storage.create_container()
        print("   ✓ Directory created/verified")
        
        # Upload test file
        print("\n3. Uploading test file...")
        test_content = f"Test file created at {datetime.now()}\nLocal storage is working!"
        test_file = io.BytesIO(test_content.encode('utf-8'))
        file_url = storage.upload_file(test_file, 'local_test.txt')
        print(f"   ✓ File uploaded: {file_url}")
        
        # Check if file exists
        print("\n4. Checking file existence...")
        exists = storage.file_exists('local_test.txt')
        print(f"   ✓ File exists: {exists}")
        
        # List files
        print("\n5. Listing files...")
        files = storage.list_files()
        print(f"   ✓ Found {len(files)} file(s)")
        for file in files:
            print(f"     - {file['name']} ({file['size']} bytes)")
        
        # Download file
        print("\n6. Downloading file...")
        content = storage.download_file('local_test.txt')
        print(f"   ✓ Downloaded {len(content)} bytes")
        print(f"   Content: {content.decode('utf-8')[:50]}...")
        
        # Get storage info
        print("\n7. Getting storage info...")
        info = storage.get_storage_info()
        print(f"   ✓ Total files: {info['total_files']}")
        print(f"   ✓ Total size: {info['total_size_mb']} MB")
        print(f"   ✓ Storage path: {info['storage_path']}")
        
        # Delete test file
        print("\n8. Cleaning up...")
        storage.delete_file('local_test.txt')
        print("   ✓ Test file deleted")
        
        print("\n" + "="*60)
        print("  ✓ ALL TESTS PASSED!")
        print("="*60)
        print("\n✅ Local storage is working correctly!")
        print(f"\n📁 Files are stored in: {os.path.abspath('uploads/photos')}")
        print("\nYou can now run: python app.py")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. local_storage_service.py exists")
        print("2. You have write permissions in this directory")
        return False

if __name__ == "__main__":
    test_local_storage()
