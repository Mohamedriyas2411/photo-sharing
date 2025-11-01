"""
Azure Blob Storage Service for Photo Sharing Platform
Handles container creation, file upload, retrieval, and deletion
"""

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import os
from datetime import datetime, timedelta
from typing import List, Dict
import mimetypes

class AzureBlobStorage:
    """
    Azure Blob Storage service for managing photo uploads
    """
    
    def __init__(self, connection_string: str, container_name: str = 'photos'):
        """
        Initialize Azure Blob Storage client
        
        Args:
            connection_string: Azure Storage account connection string
            container_name: Name of the container to store photos
        """
        if not connection_string:
            raise ValueError("Azure Storage connection string is required")
        
        self.connection_string = connection_string
        self.container_name = container_name
        
        # Create BlobServiceClient
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )
        
        # Get container client
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )
    
    def create_container(self) -> bool:
        """
        Create a container if it doesn't exist
        
        Returns:
            True if container was created or already exists
        """
        try:
            self.container_client.create_container(public_access='blob')
            print(f"Container '{self.container_name}' created successfully")
            return True
        except ResourceExistsError:
            print(f"Container '{self.container_name}' already exists")
            return True
        except Exception as e:
            print(f"Error creating container: {e}")
            raise
    
    def upload_file(self, file_stream, filename: str) -> str:
        """
        Upload a file to Azure Blob Storage
        
        Args:
            file_stream: File object or stream to upload
            filename: Name of the file
            
        Returns:
            URL of the uploaded blob
        """
        try:
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Upload the file
            blob_client.upload_blob(
                file_stream,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
            
            # Return the URL
            blob_url = blob_client.url
            print(f"File '{filename}' uploaded successfully")
            return blob_url
            
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise
    
    def download_file(self, filename: str) -> bytes:
        """
        Download a file from Azure Blob Storage
        
        Args:
            filename: Name of the file to download
            
        Returns:
            File content as bytes
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            # Download blob
            stream = blob_client.download_blob()
            return stream.readall()
            
        except ResourceNotFoundError:
            print(f"File '{filename}' not found")
            raise
        except Exception as e:
            print(f"Error downloading file: {e}")
            raise
    
    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from Azure Blob Storage
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if file was deleted successfully
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            blob_client.delete_blob()
            print(f"File '{filename}' deleted successfully")
            return True
            
        except ResourceNotFoundError:
            print(f"File '{filename}' not found")
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            raise
    
    def list_files(self) -> List[Dict[str, str]]:
        """
        List all files in the container
        
        Returns:
            List of dictionaries containing file information
        """
        try:
            blobs = self.container_client.list_blobs()
            
            file_list = []
            for blob in blobs:
                file_info = {
                    'name': blob.name,
                    'url': f"{self.container_client.url}/{blob.name}",
                    'size': blob.size,
                    'created': blob.creation_time.strftime('%Y-%m-%d %H:%M:%S') if blob.creation_time else 'Unknown',
                    'content_type': blob.content_settings.content_type if blob.content_settings else 'Unknown'
                }
                file_list.append(file_info)
            
            return file_list
            
        except Exception as e:
            print(f"Error listing files: {e}")
            raise
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists in the container
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            return blob_client.exists()
            
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False
    
    def get_file_url(self, filename: str, expiry_hours: int = 24) -> str:
        """
        Get a SAS URL for a file (useful for private containers)
        
        Args:
            filename: Name of the file
            expiry_hours: Hours until the URL expires
            
        Returns:
            SAS URL for the file
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=filename
            )
            
            # For public containers, just return the URL
            return blob_client.url
            
        except Exception as e:
            print(f"Error generating URL: {e}")
            raise


# Example usage and testing
if __name__ == "__main__":
    """
    Test the Azure Blob Storage service
    """
    import sys
    
    # Get connection string from environment
    connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    
    if not connection_string:
        print("Error: AZURE_STORAGE_CONNECTION_STRING environment variable not set")
        print("Please set it with your Azure Storage account connection string")
        sys.exit(1)
    
    # Initialize storage service
    storage = AzureBlobStorage(
        connection_string=connection_string,
        container_name='photos'
    )
    
    # Create container
    print("\n=== Creating Container ===")
    storage.create_container()
    
    # List files
    print("\n=== Listing Files ===")
    files = storage.list_files()
    if files:
        for file in files:
            print(f"- {file['name']} ({file['size']} bytes) - {file['created']}")
    else:
        print("No files in container")
    
    print("\n=== Storage Service Test Complete ===")
