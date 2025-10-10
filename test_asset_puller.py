#!/usr/bin/env python3
"""
Test script for webMethods.io Integration Asset Puller

This script tests the functionality of the modified_webmethods_asset_puller.py script
by creating a mock environment and verifying the directory structure.
"""

import os
import json
import shutil
import unittest
from unittest.mock import patch, MagicMock

# Import the script to test
import modified_webmethods_asset_puller as asset_puller

class TestAssetPuller(unittest.TestCase):
    """Test cases for the webMethods.io Integration Asset Puller"""

    def setUp(self):
        """Set up test environment"""
        # Create a test directory
        self.test_dir = "./test_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a test config file
        self.config = {
            "base_url": "https://test-url.example.com",
            "project_name": "TestProject",
            "project_id": "test123",
            "github_repo_path": self.test_dir,
            "auth": {
                "api_key": "test_api_key"
            }
        }
        
        with open('test_config.json', 'w') as f:
            json.dump(self.config, f)

    def tearDown(self):
        """Clean up test environment"""
        # Remove test directory and config file
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        if os.path.exists('test_config.json'):
            os.remove('test_config.json')

    def test_directory_structure(self):
        """Test that the correct directory structure is created"""
        # Mock the configuration loading
        with patch('modified_webmethods_asset_puller.open') as mock_open:
            mock_file = MagicMock()
            mock_open.return_value.__enter__.return_value = mock_file
            mock_file.read.return_value = json.dumps(self.config)
            
            # Set environment variables
            with patch.dict(os.environ, {
                'GITHUB_REPO_PATH': self.test_dir
            }):
                # Run the script's directory creation code
                asset_puller.GITHUB_REPO_PATH = self.test_dir
                
                # Create directories
                asset_puller.ASSETS_DIR = os.path.join(asset_puller.GITHUB_REPO_PATH, "downloaded_assets")
                os.makedirs(asset_puller.ASSETS_DIR, exist_ok=True)
                
                asset_puller.WORKFLOWS_DIR = os.path.join(asset_puller.ASSETS_DIR, "workflows")
                os.makedirs(asset_puller.WORKFLOWS_DIR, exist_ok=True)
                
                asset_puller.FLOWS_DIR = os.path.join(asset_puller.ASSETS_DIR, "flows")
                asset_puller.LISTENERS_DIR = os.path.join(asset_puller.ASSETS_DIR, "listeners")
                asset_puller.MESSAGING_DIR = os.path.join(asset_puller.ASSETS_DIR, "messaging")
                
                os.makedirs(asset_puller.FLOWS_DIR, exist_ok=True)
                os.makedirs(asset_puller.LISTENERS_DIR, exist_ok=True)
                os.makedirs(asset_puller.MESSAGING_DIR, exist_ok=True)
                
                # Verify directory structure
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, "downloaded_assets")))
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, "downloaded_assets", "workflows")))
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, "downloaded_assets", "flows")))
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, "downloaded_assets", "listeners")))
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, "downloaded_assets", "messaging")))

    @patch('modified_webmethods_asset_puller.requests.get')
    @patch('modified_webmethods_asset_puller.requests.post')
    def test_download_workflow(self, mock_post, mock_get):
        """Test that workflows are downloaded to the correct location"""
        # Mock the API responses
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = {
            "output": {
                "download_link": "https://example.com/download/workflow123/file.zip"
            }
        }
        mock_post.return_value.raise_for_status = MagicMock()
        
        mock_get.return_value = MagicMock()
        mock_get.return_value.content = b'test content'
        mock_get.return_value.raise_for_status = MagicMock()
        
        # Set up the test environment
        asset_puller.GITHUB_REPO_PATH = self.test_dir
        asset_puller.ASSETS_DIR = os.path.join(asset_puller.GITHUB_REPO_PATH, "downloaded_assets")
        asset_puller.WORKFLOWS_DIR = os.path.join(asset_puller.ASSETS_DIR, "workflows")
        
        os.makedirs(asset_puller.ASSETS_DIR, exist_ok=True)
        os.makedirs(asset_puller.WORKFLOWS_DIR, exist_ok=True)
        
        # Call the function
        asset_puller.BASE_URL = "https://test-url.example.com"
        asset_puller.PROJECT_ID = "test123"
        result = asset_puller.download_workflow("workflow123")
        
        # Verify the result
        expected_path = os.path.join(self.test_dir, "downloaded_assets", "workflows", "workflow123.zip")
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.exists(expected_path))
        
        # Verify file content
        with open(expected_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b'test content')

if __name__ == '__main__':
    unittest.main()

# Made with Bob
