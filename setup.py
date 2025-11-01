"""
Quick Setup Script for Photo Sharing Platform
Run this after setting up your .env file
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    load_dotenv()
    
    required_vars = {
        'AZURE_STORAGE_CONNECTION_STRING': 'Azure Storage connection string',
        'AZURE_CONTAINER_NAME': 'Container name (optional, defaults to "photos")',
    }
    
    print("=" * 60)
    print("Photo Sharing Platform - Environment Check")
    print("=" * 60)
    print()
    
    all_set = True
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'CONNECTION_STRING' in var or 'KEY' in var:
                display_value = f"{value[:20]}...{value[-10:]}" if len(value) > 30 else "***"
            else:
                display_value = value
            print(f"✓ {var}")
            print(f"  {description}")
            print(f"  Value: {display_value}")
        else:
            print(f"✗ {var} - NOT SET")
            print(f"  {description}")
            if var == 'AZURE_STORAGE_CONNECTION_STRING':
                all_set = False
        print()
    
    return all_set

def test_storage_connection():
    """Test connection to Azure Blob Storage"""
    print("=" * 60)
    print("Testing Azure Storage Connection")
    print("=" * 60)
    print()
    
    try:
        from storage_service import AzureBlobStorage
        
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        container_name = os.environ.get('AZURE_CONTAINER_NAME', 'photos')
        
        print(f"Initializing storage service...")
        print(f"Container name: {container_name}")
        print()
        
        storage = AzureBlobStorage(
            connection_string=connection_string,
            container_name=container_name
        )
        
        print("✓ Storage client initialized successfully")
        print()
        
        # Test container creation
        print("Creating container (if it doesn't exist)...")
        storage.create_container()
        print("✓ Container ready")
        print()
        
        # Test listing files
        print("Listing files in container...")
        files = storage.list_files()
        print(f"✓ Found {len(files)} file(s) in container")
        print()
        
        if files:
            print("Files in container:")
            for i, file in enumerate(files[:5], 1):  # Show first 5
                print(f"  {i}. {file['name']} ({file['size']} bytes)")
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
        else:
            print("  (Container is empty - ready for uploads!)")
        print()
        
        print("=" * 60)
        print("✓ All tests passed! Storage is ready to use.")
        print("=" * 60)
        return True
        
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Connection Error: {e}")
        print()
        print("Common issues:")
        print("  - Check your connection string is correct")
        print("  - Verify your Azure Storage account is active")
        print("  - Ensure your network allows Azure connections")
        return False

def main():
    """Main setup function"""
    print()
    
    # Check environment
    if not check_environment():
        print("=" * 60)
        print("⚠ Setup Required")
        print("=" * 60)
        print()
        print("Please complete these steps:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your Azure Storage connection string")
        print("3. Run this script again")
        print()
        sys.exit(1)
    
    print("=" * 60)
    print("✓ Environment variables configured")
    print("=" * 60)
    print()
    
    # Test storage connection
    if test_storage_connection():
        print()
        print("Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Start uploading photos!")
        print()
    else:
        print()
        print("Please fix the errors above and try again.")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
