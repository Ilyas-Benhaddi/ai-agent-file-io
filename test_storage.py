"""
Test script for Storage Service
Run this after starting MinIO to verify everything works
"""
import sys
sys.path.append('.')

from src.storage_service import StorageService
import time

def test_storage_service():
    """Test all storage service functions"""
    
    print("🧪 Testing Storage Service...\n")
    
    # Initialize storage
    print("1️⃣ Initializing MinIO connection...")
    try:
        storage = StorageService(
            endpoint="localhost:9002",
            access_key="minioadmin",
            secret_key="minioadmin123",
            bucket_name="agent-files",
            secure=False
        )
        print("✅ Connected to MinIO successfully!\n")
    except Exception as e:
        print(f"❌ Failed to connect to MinIO: {e}")
        print("Make sure MinIO is running: docker-compose up -d")
        return
    
    # Test 1: Upload file
    print("2️⃣ Testing file upload...")
    test_content = b"Hello from the AI Agent! This is a test file."
    result = storage.upload_file(
        test_content,
        "test_file.txt",
        "text/plain"
    )
    if result["success"]:
        print(f"✅ File uploaded: {result['s3_key']}")
        print(f"   Size: {result['size']} bytes\n")
    else:
        print(f"❌ Upload failed: {result['error']}\n")
        return
    
    # Test 2: Download file
    print("3️⃣ Testing file download...")
    downloaded = storage.download_file("test_file.txt")
    if downloaded:
        print(f"✅ File downloaded: {len(downloaded)} bytes")
        print(f"   Content: {downloaded.decode()}\n")
    else:
        print("❌ Download failed\n")
    
    # Test 3: Get file metadata
    print("4️⃣ Testing file metadata...")
    metadata = storage.get_file_metadata("test_file.txt")
    if metadata:
        print(f"✅ Metadata retrieved:")
        print(f"   Name: {metadata['name']}")
        print(f"   Size: {metadata['size']} bytes")
        print(f"   Content Type: {metadata['content_type']}")
        print(f"   Last Modified: {metadata['last_modified']}\n")
    else:
        print("❌ Failed to get metadata\n")
    
    # Test 4: List files
    print("5️⃣ Testing file listing...")
    files = storage.list_files()
    print(f"✅ Found {len(files)} file(s) in bucket:")
    for file in files:
        print(f"   - {file}")
    print()
    
    # Test 5: Generate presigned URL
    print("6️⃣ Testing presigned URL generation...")
    url = storage.generate_presigned_url("test_file.txt")
    if url:
        print(f"✅ Presigned URL generated:")
        print(f"   {url[:80]}...\n")
    else:
        print("❌ Failed to generate URL\n")
    
    # Test 6: Delete file
    print("7️⃣ Testing file deletion...")
    if storage.delete_file("test_file.txt"):
        print("✅ File deleted successfully\n")
    else:
        print("❌ Deletion failed\n")
    
    # Verify deletion
    print("8️⃣ Verifying deletion...")
    files_after = storage.list_files()
    if "test_file.txt" not in files_after:
        print("✅ File confirmed deleted\n")
    else:
        print("❌ File still exists\n")
    
    print("=" * 50)
    print("🎉 All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_storage_service()
