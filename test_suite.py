"""
Comprehensive Test Suite for Photo Sharing Platform
Tests all storage operations and validates setup
"""

import os
import sys
import io
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"  {text}")

class TestSuite:
    """Test suite for storage operations"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.storage = None
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results"""
        print(f"\n{Colors.BOLD}Test: {test_name}{Colors.END}")
        try:
            result = test_func()
            if result:
                print_success(f"{test_name} - PASSED")
                self.passed += 1
            else:
                print_error(f"{test_name} - FAILED")
                self.failed += 1
            return result
        except Exception as e:
            print_error(f"{test_name} - ERROR: {e}")
            self.failed += 1
            return False
    
    def test_environment_variables(self):
        """Test if required environment variables are set"""
        print_info("Checking environment variables...")
        
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        container_name = os.environ.get('AZURE_CONTAINER_NAME', 'photos')
        
        if not connection_string:
            print_error("AZURE_STORAGE_CONNECTION_STRING not set")
            print_info("Please set this in your .env file")
            return False
        
        print_success("AZURE_STORAGE_CONNECTION_STRING is set")
        print_info(f"Container name: {container_name}")
        return True
    
    def test_import_dependencies(self):
        """Test if all required dependencies are installed"""
        print_info("Checking dependencies...")
        
        dependencies = [
            ('Flask', 'flask'),
            ('Azure Storage Blob', 'azure.storage.blob'),
            ('Python-dotenv', 'dotenv'),
            ('Werkzeug', 'werkzeug'),
        ]
        
        all_installed = True
        for name, module in dependencies:
            try:
                __import__(module)
                print_success(f"{name} installed")
            except ImportError:
                print_error(f"{name} NOT installed")
                all_installed = False
        
        return all_installed
    
    def test_storage_initialization(self):
        """Test Azure Storage service initialization"""
        print_info("Initializing storage service...")
        
        try:
            from storage_service import AzureBlobStorage
            
            connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
            container_name = os.environ.get('AZURE_CONTAINER_NAME', 'photos')
            
            self.storage = AzureBlobStorage(
                connection_string=connection_string,
                container_name=container_name
            )
            
            print_success("Storage service initialized")
            return True
        except Exception as e:
            print_error(f"Failed to initialize: {e}")
            return False
    
    def test_container_creation(self):
        """Test container creation"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        print_info("Creating/verifying container...")
        
        try:
            result = self.storage.create_container()
            print_success(f"Container '{self.storage.container_name}' ready")
            return True
        except Exception as e:
            print_error(f"Container creation failed: {e}")
            return False
    
    def test_file_upload(self):
        """Test file upload operation"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        print_info("Testing file upload...")
        
        try:
            # Create a test file
            test_content = f"Test file created at {datetime.now()}"
            test_file = io.BytesIO(test_content.encode('utf-8'))
            test_filename = "test_upload.txt"
            
            # Upload file
            blob_url = self.storage.upload_file(test_file, test_filename)
            
            print_success(f"File uploaded: {test_filename}")
            print_info(f"URL: {blob_url}")
            
            # Store filename for later tests
            self.test_filename = test_filename
            return True
        except Exception as e:
            print_error(f"Upload failed: {e}")
            return False
    
    def test_file_exists(self):
        """Test file existence check"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        if not hasattr(self, 'test_filename'):
            print_warning("No test file uploaded, skipping")
            self.skipped += 1
            return False
        
        print_info(f"Checking if '{self.test_filename}' exists...")
        
        try:
            exists = self.storage.file_exists(self.test_filename)
            if exists:
                print_success(f"File exists: {self.test_filename}")
                return True
            else:
                print_error(f"File not found: {self.test_filename}")
                return False
        except Exception as e:
            print_error(f"Existence check failed: {e}")
            return False
    
    def test_file_listing(self):
        """Test file listing operation"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        print_info("Listing files in container...")
        
        try:
            files = self.storage.list_files()
            print_success(f"Found {len(files)} file(s)")
            
            if files:
                print_info("Files in container:")
                for i, file in enumerate(files[:5], 1):
                    print_info(f"  {i}. {file['name']} ({file['size']} bytes)")
                if len(files) > 5:
                    print_info(f"  ... and {len(files) - 5} more")
            
            return True
        except Exception as e:
            print_error(f"Listing failed: {e}")
            return False
    
    def test_file_download(self):
        """Test file download operation"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        if not hasattr(self, 'test_filename'):
            print_warning("No test file uploaded, skipping")
            self.skipped += 1
            return False
        
        print_info(f"Downloading '{self.test_filename}'...")
        
        try:
            content = self.storage.download_file(self.test_filename)
            print_success(f"Downloaded {len(content)} bytes")
            print_info(f"Content preview: {content[:50].decode('utf-8', errors='ignore')}...")
            return True
        except Exception as e:
            print_error(f"Download failed: {e}")
            return False
    
    def test_file_deletion(self):
        """Test file deletion operation"""
        if not self.storage:
            print_warning("Storage not initialized, skipping")
            self.skipped += 1
            return False
        
        if not hasattr(self, 'test_filename'):
            print_warning("No test file to delete, skipping")
            self.skipped += 1
            return False
        
        print_info(f"Deleting '{self.test_filename}'...")
        
        try:
            result = self.storage.delete_file(self.test_filename)
            if result:
                print_success(f"File deleted: {self.test_filename}")
                return True
            else:
                print_error("Delete returned False")
                return False
        except Exception as e:
            print_error(f"Deletion failed: {e}")
            return False
    
    def test_flask_app_imports(self):
        """Test if Flask app can be imported"""
        print_info("Testing Flask app imports...")
        
        try:
            import app
            print_success("Flask app imported successfully")
            
            # Check for required routes
            routes = ['index', 'upload_file', 'gallery', 'delete_file', 'health']
            all_routes_exist = True
            
            for route in routes:
                if hasattr(app, route):
                    print_success(f"Route '{route}' found")
                else:
                    print_error(f"Route '{route}' NOT found")
                    all_routes_exist = False
            
            return all_routes_exist
        except Exception as e:
            print_error(f"Failed to import app: {e}")
            return False
    
    def test_templates_exist(self):
        """Test if template files exist"""
        print_info("Checking template files...")
        
        templates = ['templates/index.html', 'templates/gallery.html']
        all_exist = True
        
        for template in templates:
            if os.path.exists(template):
                print_success(f"{template} exists")
            else:
                print_error(f"{template} NOT found")
                all_exist = False
        
        return all_exist
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total = self.passed + self.failed + self.skipped
        
        print(f"{Colors.BOLD}Total Tests:{Colors.END} {total}")
        print(f"{Colors.GREEN}Passed:{Colors.END} {self.passed}")
        print(f"{Colors.RED}Failed:{Colors.END} {self.failed}")
        print(f"{Colors.YELLOW}Skipped:{Colors.END} {self.skipped}")
        
        if self.failed == 0 and self.passed > 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}")
            print(f"\n{Colors.BOLD}Your application is ready to use!{Colors.END}")
            print("\nNext steps:")
            print("  1. Run: python app.py")
            print("  2. Open: http://localhost:5000")
            print("  3. Start uploading photos!")
        elif self.failed > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}")
            print("\nPlease fix the errors above before proceeding.")
        else:
            print(f"\n{Colors.YELLOW}⚠ NO TESTS RUN{Colors.END}")

def main():
    """Main test runner"""
    print_header("PHOTO SHARING PLATFORM - TEST SUITE")
    print(f"{Colors.BOLD}Running comprehensive tests...{Colors.END}")
    
    suite = TestSuite()
    
    # Run all tests
    tests = [
        ("Environment Variables", suite.test_environment_variables),
        ("Import Dependencies", suite.test_import_dependencies),
        ("Storage Initialization", suite.test_storage_initialization),
        ("Container Creation", suite.test_container_creation),
        ("File Upload", suite.test_file_upload),
        ("File Existence Check", suite.test_file_exists),
        ("File Listing", suite.test_file_listing),
        ("File Download", suite.test_file_download),
        ("File Deletion", suite.test_file_deletion),
        ("Flask App Imports", suite.test_flask_app_imports),
        ("Template Files", suite.test_templates_exist),
    ]
    
    for test_name, test_func in tests:
        suite.run_test(test_name, test_func)
    
    # Print summary
    suite.print_summary()
    
    # Return exit code
    sys.exit(0 if suite.failed == 0 else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)
