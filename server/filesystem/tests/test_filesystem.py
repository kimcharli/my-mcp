#!/usr/bin/env python3
"""
Tests for the filesystem MCP server functionality.
"""
import os
import tempfile
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

# Import the modules to test
from filesystem import (
    disk_usage_summary, find_large_files, analyze_directory_sizes,
    clean_temp_files, clean_downloads_folder, clear_application_caches,
    find_duplicate_files, list_installed_applications,
    format_size, get_creation_time, is_system_file, get_directory_size
)


class TestFilesystemServer(unittest.TestCase):
    """Test cases for the filesystem server functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        
        # Create a test file
        with open(self.test_file_path, 'w') as f:
            f.write("Test content for file operations")
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

    def test_format_size(self):
        """Test the format_size utility function."""
        self.assertEqual(format_size(1024), '1.0 kB')
        self.assertEqual(format_size(1048576), '1.0 MB')
        self.assertEqual(format_size(0), '0 Bytes')

    def test_get_creation_time(self):
        """Test getting file creation time."""
        # Test with existing file
        ctime = get_creation_time(self.test_file_path)
        self.assertIsInstance(ctime, float)
        self.assertGreater(ctime, 0)
        
        # Test with non-existing file
        non_existing = "/path/that/does/not/exist"
        ctime = get_creation_time(non_existing)
        self.assertEqual(ctime, 0)

    def test_is_system_file(self):
        """Test system file detection."""
        # System paths should return True
        self.assertTrue(is_system_file("/System/Library/test"))
        self.assertTrue(is_system_file("/bin/bash"))
        self.assertTrue(is_system_file("/usr/bin/python"))
        
        # User paths should return False
        self.assertFalse(is_system_file("/Users/test/file.txt"))
        self.assertFalse(is_system_file("/tmp/test"))

    def test_is_safe_path(self):
        """Test safe path validation."""
        # Safe paths should return True
        self.assertTrue(is_safe_path(os.path.expanduser("~")))
        self.assertTrue(is_safe_path(os.path.join(os.path.expanduser("~"), "test")))

        # Unsafe paths should return False
        self.assertFalse(is_safe_path("/"))
        self.assertFalse(is_safe_path("/etc/passwd"))

    def test_get_directory_size(self):
        """Test directory size calculation."""
        # Test with temp directory
        size = get_directory_size(self.temp_dir)
        self.assertIsInstance(size, int)
        self.assertGreater(size, 0)  # Should have at least our test file
        
        # Test with non-existing directory
        non_existing = "/path/that/does/not/exist"
        size = get_directory_size(non_existing)
        self.assertEqual(size, 0)

    @patch('psutil.disk_partitions')
    @patch('psutil.disk_usage')
    @pytest.mark.asyncio
    async def test_disk_usage_summary(self, mock_disk_usage, mock_disk_partitions):
        """Test disk usage summary function."""
        # Mock data
        mock_partition = MagicMock()
        mock_partition.device = '/dev/disk1s1'
        mock_partition.mountpoint = '/'
        mock_partition.fstype = 'apfs'
        mock_disk_partitions.return_value = [mock_partition]
        
        mock_usage = MagicMock()
        mock_usage.total = 1000000000000  # 1TB
        mock_usage.used = 500000000000   # 500GB
        mock_usage.free = 500000000000   # 500GB
        mock_usage.percent = 50.0
        mock_disk_usage.return_value = mock_usage
        
        result = await disk_usage_summary()
        
        self.assertIn('Disk: /dev/disk1s1', result)
        self.assertIn('Mount point: /', result)
        self.assertIn('File system type: apfs', result)
        self.assertIn('Total: 1.0 TB', result)
        self.assertIn('Used: 500.0 GB (50.0%)', result)
        
        mock_disk_partitions.assert_called_once()
        mock_disk_usage.assert_called_once_with('/')

    @patch('os.walk')
    @patch('os.path.getsize')
    @pytest.mark.asyncio
    async def test_find_large_files(self, mock_getsize, mock_walk):
        """Test finding large files."""
        # Mock directory walk
        mock_walk.return_value = [
            ('/test', [], ['large_file.txt', 'small_file.txt'])
        ]
        
        # Mock file sizes
        def mock_size_func(path):
            if 'large_file.txt' in path:
                return 200 * 1024 * 1024  # 200MB
            else:
                return 1024  # 1KB
        
        mock_getsize.side_effect = mock_size_func
        
        result = await find_large_files(min_size_mb=100, directory='/test')
        
        self.assertIn('large_file.txt', result)
        self.assertIn('200.0 MB', result)
        self.assertNotIn('small_file.txt', result)

    @patch('filesystem.get_directory_size')
    @pytest.mark.asyncio
    async def test_analyze_directory_sizes(self, mock_get_dir_size):
        """Test directory size analysis."""
        # Mock directory sizes
        mock_get_dir_size.side_effect = [
            1000000000,  # 1GB for first directory
            500000000,   # 500MB for second
            100000000    # 100MB for third
        ]
        
        with patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ['dir1', 'dir2', 'dir3']
            
            with patch('os.path.isdir') as mock_isdir:
                mock_isdir.return_value = True
                
                result = await analyze_directory_sizes(top_n=3)
                
                self.assertIn('dir1', result)
                self.assertIn('1.0 GB', result)
                self.assertIn('dir2', result)
                self.assertIn('500.0 MB', result)

    @patch('os.walk')
    @patch('send2trash.send2trash')
    @pytest.mark.asyncio
    async def test_clean_temp_files(self, mock_send2trash, mock_walk):
        """Test cleaning temporary files."""
        # Mock finding temp files
        mock_walk.return_value = [
            ('/tmp', [], ['temp1.tmp', 'temp2.cache', 'important.txt'])
        ]
        
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            
            # Test dry run
            result = await clean_temp_files(dry_run=True)
            self.assertIn('temp1.tmp', result)
            self.assertIn('temp2.cache', result)
            mock_send2trash.assert_not_called()
            
            # Test actual cleanup
            result = await clean_temp_files(dry_run=False)
            self.assertIn('Cleaned', result)
            # Should be called for temp files only
            self.assertEqual(mock_send2trash.call_count, 2)

    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('send2trash.send2trash')
    @pytest.mark.asyncio
    async def test_clean_downloads_folder(self, mock_send2trash, mock_getmtime, mock_listdir):
        """Test cleaning downloads folder."""
        # Mock old and new files
        mock_listdir.return_value = ['old_file.zip', 'new_file.pdf']
        
        import time
        current_time = time.time()
        
        def mock_mtime(path):
            if 'old_file.zip' in path:
                return current_time - (40 * 24 * 3600)  # 40 days old
            else:
                return current_time - (5 * 24 * 3600)   # 5 days old
        
        mock_getmtime.side_effect = mock_mtime
        
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            
            # Test with 30 days threshold
            result = await clean_downloads_folder(days_old=30, dry_run=False)
            
            self.assertIn('old_file.zip', result)
            mock_send2trash.assert_called_once()

    @pytest.mark.asyncio
    async def test_clear_application_caches_invalid_app(self):
        """Test clearing caches for invalid application."""
        result = await clear_application_caches(app_name="NonExistentApp", dry_run=True)
        self.assertIn('not found', result)

    @patch('os.walk')
    @patch('hashlib.md5')
    @pytest.mark.asyncio
    async def test_find_duplicate_files(self, mock_md5, mock_walk):
        """Test finding duplicate files."""
        # Mock file structure
        mock_walk.return_value = [
            ('/test', [], ['file1.txt', 'file2.txt', 'file3.txt'])
        ]
        
        # Mock hash calculation - file1 and file3 are duplicates
        mock_hash_obj = MagicMock()
        mock_hash_obj.hexdigest.side_effect = ['hash1', 'hash2', 'hash1']
        mock_md5.return_value = mock_hash_obj
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b'content'
            
            result = await find_duplicate_files(directory='/test', max_files=100)
            
            self.assertIn('Duplicate files found', result)
            self.assertIn('file1.txt', result)
            self.assertIn('file3.txt', result)

    @patch('os.listdir')
    @patch('filesystem.get_directory_size')
    @pytest.mark.asyncio
    async def test_list_installed_applications(self, mock_get_dir_size, mock_listdir):
        """Test listing installed applications."""
        # Mock applications directory
        mock_listdir.return_value = ['App1.app', 'App2.app', 'NotAnApp.txt']
        
        # Mock app sizes
        mock_get_dir_size.side_effect = [100000000, 50000000]  # 100MB, 50MB
        
        with patch('os.path.isdir') as mock_isdir:
            def mock_isdir_func(path):
                return path.endswith('.app')
            mock_isdir.side_effect = mock_isdir_func
            
            result = await list_installed_applications()
            
            self.assertIn('App1.app', result)
            self.assertIn('100.0 MB', result)
            self.assertIn('App2.app', result)
            self.assertIn('50.0 MB', result)
            self.assertNotIn('NotAnApp.txt', result)


if __name__ == '__main__':
    unittest.main()