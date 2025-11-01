"""
Local File Storage Service for Photo Sharing Platform
Alternative to Azure Blob Storage - stores files locally on the system
"""

import os
import shutil
from datetime import datetime
from typing import List, Dict
import mimetypes
from pathlib import Path

class LocalFileStorage:
    """
    Local file storage service for managing photo uploads
    Stores files in a local directory instead of cloud
    """
    
    def __init__(self, storage_path: str = 'uploads', container_name: str = 'photos'):
        """
        Initialize Local File Storage
        
        Args:
            storage_path: Base directory for file storage
            container_name: Subdirectory name (acts like Azure container)
        """
        self.storage_path = storage_path
        self.container_name = container_name
        
        # Full path to storage directory
        self.full_path = os.path.join(storage_path, container_name)
        
        print(f"Local storage initialized: {self.full_path}")
    
    def create_container(self) -> bool:
        """
        Create storage directory if it doesn't exist
        (Equivalent to Azure container creation)
        
        Returns:
            True if directory was created or already exists
        """
        try:
            os.makedirs(self.full_path, exist_ok=True)
            print(f"Storage directory '{self.full_path}' ready")
            return True
        except Exception as e:
            print(f"Error creating storage directory: {e}")
            raise
    
    def upload_file(self, file_stream, filename: str) -> str:
        """
        Save a file to local storage
        
        Args:
            file_stream: File object or stream to save
            filename: Name of the file
            
        Returns:
            Local file path (acts as URL)
        """
        try:
            # Ensure directory exists
            self.create_container()
            
            # Full file path
            file_path = os.path.join(self.full_path, filename)
            
            # Save the file
            with open(file_path, 'wb') as f:
                if hasattr(file_stream, 'read'):
                    # It's a file-like object
                    shutil.copyfileobj(file_stream, f)
                else:
                    # It's bytes
                    f.write(file_stream)
            
            print(f"File '{filename}' saved to {file_path}")
            
            # Return relative path (acts as URL for web access)
            return f"/{self.storage_path}/{self.container_name}/{filename}"
            
        except Exception as e:
            print(f"Error saving file: {e}")
            raise
    
    def download_file(self, filename: str) -> bytes:
        """
        Read a file from local storage
        
        Args:
            filename: Name of the file to read
            
        Returns:
            File content as bytes
        """
        try:
            file_path = os.path.join(self.full_path, filename)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{filename}' not found")
            
            with open(file_path, 'rb') as f:
                return f.read()
                
        except FileNotFoundError:
            print(f"File '{filename}' not found")
            raise
        except Exception as e:
            print(f"Error reading file: {e}")
            raise
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from local storage
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if file was deleted successfully
        """
        try:
            file_path = os.path.join(self.full_path, filename)
            
            if not os.path.exists(file_path):
                print(f"File '{filename}' not found")
                return False
            
            os.remove(file_path)
            print(f"File '{filename}' deleted successfully")
            return True
            
        except Exception as e:
            print(f"Error deleting file: {e}")
            raise
    
    def list_files(self) -> List[Dict[str, str]]:
        """
        List all files in the storage directory
        
        Returns:
            List of dictionaries containing file information
        """
        try:
            # Ensure directory exists
            if not os.path.exists(self.full_path):
                return []
            
            file_list = []
            
            for filename in os.listdir(self.full_path):
                file_path = os.path.join(self.full_path, filename)
                
                # Skip if it's a directory
                if os.path.isdir(file_path):
                    continue
                
                # Get file stats
                stats = os.stat(file_path)
                
                # Get content type
                content_type, _ = mimetypes.guess_type(filename)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                file_info = {
                    'name': filename,
                    'url': f"/{self.storage_path}/{self.container_name}/{filename}",
                    'size': stats.st_size,
                    'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    'content_type': content_type
                }
                file_list.append(file_info)
            
            # Sort by creation time (newest first)
            file_list.sort(key=lambda x: x['created'], reverse=True)
            
            return file_list
            
        except Exception as e:
            print(f"Error listing files: {e}")
            raise
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists in storage
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            file_path = os.path.join(self.full_path, filename)
            return os.path.exists(file_path)
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False
    
    def get_file_url(self, filename: str, expiry_hours: int = 24) -> str:
        """
        Get URL for a file (for compatibility with Azure version)
        
        Args:
            filename: Name of the file
            expiry_hours: Not used in local storage (kept for compatibility)
            
        Returns:
            Local file path/URL
        """
        return f"/{self.storage_path}/{self.container_name}/{filename}"
    
    def get_storage_info(self) -> Dict[str, any]:
        """
        Get information about storage usage
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            if not os.path.exists(self.full_path):
                return {
                    'total_files': 0,
                    'total_size': 0,
                    'storage_path': self.full_path
                }
            
            files = self.list_files()
            total_size = sum(f['size'] for f in files)
            
            return {
                'total_files': len(files),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'storage_path': self.full_path,
                'storage_type': 'local'
            }
        except Exception as e:
            print(f"Error getting storage info: {e}")
            return {
                'total_files': 0,
                'total_size': 0,
                'error': str(e)
            }


# Example usage and testing
if __name__ == "__main__":
    """
    Test the Local File Storage service
    """
    import io
    
    print("\n" + "="*60)
    print("  LOCAL FILE STORAGE TEST")
    print("="*60 + "\n")
    
    # Initialize storage service
    storage = LocalFileStorage(
        storage_path='uploads',
        container_name='photos'
    )
    
    # Create storage directory
    print("\n=== Creating Storage Directory ===")
    storage.create_container()
    
    # Create a test file
    print("\n=== Uploading Test File ===")
    test_content = f"Test file created at {datetime.now()}\n"
    test_file = io.BytesIO(test_content.encode('utf-8'))
    file_url = storage.upload_file(test_file, 'test_file.txt')
    print(f"File URL: {file_url}")
    
    # List files
    print("\n=== Listing Files ===")
    files = storage.list_files()
    if files:
        for file in files:
            print(f"- {file['name']} ({file['size']} bytes) - {file['created']}")
    else:
        print("No files in storage")
    
    # Check file exists
    print("\n=== Checking File Existence ===")
    exists = storage.file_exists('test_file.txt')
    print(f"test_file.txt exists: {exists}")
    
    # Download file
    print("\n=== Downloading File ===")
    content = storage.download_file('test_file.txt')
    print(f"Content: {content.decode('utf-8')}")
    
    # Get storage info
    print("\n=== Storage Information ===")
    info = storage.get_storage_info()
    print(f"Total files: {info['total_files']}")
    print(f"Total size: {info['total_size_mb']} MB")
    print(f"Storage path: {info['storage_path']}")
    
    # Clean up (optional)
    print("\n=== Cleanup ===")
    choice = input("Delete test file? (y/n): ")
    if choice.lower() == 'y':
        storage.delete_file('test_file.txt')
        print("Test file deleted")
    
    print("\n" + "="*60)
    print("  TEST COMPLETE")
    print("="*60 + "\n")
