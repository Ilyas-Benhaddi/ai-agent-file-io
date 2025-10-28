"""
Storage Service Module
Handles file operations with MinIO (S3-compatible storage)
"""
import os
import io
from typing import Optional, BinaryIO
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageService:
    """Manages file storage operations using MinIO"""
    
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False
    ):
        """
        Initialize MinIO client
        
        Args:
            endpoint: MinIO server endpoint (e.g., 'localhost:9000')
            access_key: MinIO access key
            secret_key: MinIO secret key
            bucket_name: Default bucket name
            secure: Use HTTPS if True
        """
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created successfully")
            else:
                logger.info(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")
            raise
    
    def upload_file(
        self,
        file_data: bytes,
        object_name: str,
        content_type: str = "application/octet-stream"
    ) -> dict:
        """
        Upload a file to MinIO
        
        Args:
            file_data: File content as bytes
            object_name: Name for the object in storage
            content_type: MIME type of the file
            
        Returns:
            dict: Upload result with S3 key and metadata
        """
        try:
            file_stream = io.BytesIO(file_data)
            file_size = len(file_data)
            
            result = self.client.put_object(
                self.bucket_name,
                object_name,
                file_stream,
                file_size,
                content_type=content_type
            )
            
            logger.info(f"File uploaded successfully: {object_name}")
            
            return {
                "success": True,
                "s3_key": object_name,
                "bucket": self.bucket_name,
                "size": file_size,
                "etag": result.etag
            }
        except S3Error as e:
            logger.error(f"Error uploading file: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_file(self, object_name: str) -> Optional[bytes]:
        """
        Download a file from MinIO
        
        Args:
            object_name: Name of the object to download
            
        Returns:
            bytes: File content or None if error
        """
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"File downloaded successfully: {object_name}")
            return data
        except S3Error as e:
            logger.error(f"Error downloading file: {e}")
            return None
    
    def delete_file(self, object_name: str) -> bool:
        """
        Delete a file from MinIO
        
        Args:
            object_name: Name of the object to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"File deleted successfully: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def list_files(self, prefix: str = "") -> list:
        """
        List files in the bucket
        
        Args:
            prefix: Filter objects by prefix
            
        Returns:
            list: List of object names
        """
        try:
            objects = self.client.list_objects(self.bucket_name, prefix=prefix)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    def get_file_metadata(self, object_name: str) -> Optional[dict]:
        """
        Get metadata for a file
        
        Args:
            object_name: Name of the object
            
        Returns:
            dict: File metadata or None if error
        """
        try:
            stat = self.client.stat_object(self.bucket_name, object_name)
            return {
                "name": object_name,
                "size": stat.size,
                "last_modified": stat.last_modified,
                "content_type": stat.content_type,
                "etag": stat.etag
            }
        except S3Error as e:
            logger.error(f"Error getting file metadata: {e}")
            return None
    
    def generate_presigned_url(
        self,
        object_name: str,
        expires: timedelta = timedelta(hours=1)
    ) -> Optional[str]:
        """
        Generate a presigned URL for temporary file access
        
        Args:
            object_name: Name of the object
            expires: URL expiration time
            
        Returns:
            str: Presigned URL or None if error
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
            logger.info(f"Generated presigned URL for: {object_name}")
            return url
        except S3Error as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
