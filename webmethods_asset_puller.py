#!/usr/bin/env python3
"""
webMethods.io Integration Asset Puller

This script pulls assets from webMethods.io Integration project tenant and saves them to GitHub.
"""

import os
import requests
import json
import time
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("webmethods_asset_puller.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configuration from environment variables or config file
try:
    # First try to get configuration from environment variables
    BASE_URL = os.environ.get('WEBMETHODS_BASE_URL')
    PROJECT_NAME = os.environ.get('WEBMETHODS_PROJECT_NAME')
    PROJECT_ID = os.environ.get('WEBMETHODS_PROJECT_ID')
    GITHUB_REPO_PATH = os.environ.get('GITHUB_REPO_PATH', './github_repo')
    API_KEY = os.environ.get('WEBMETHODS_API_KEY')
    
    # If environment variables are not set, try to load from config file
    if not all([BASE_URL, PROJECT_NAME, PROJECT_ID]):
        logger.info("Environment variables not found, trying to load from config.json")
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            BASE_URL = BASE_URL or config.get('base_url')
            PROJECT_NAME = PROJECT_NAME or config.get('project_name')
            PROJECT_ID = PROJECT_ID or config.get('project_id')
            GITHUB_REPO_PATH = GITHUB_REPO_PATH or config.get('github_repo_path')
            API_KEY = API_KEY or config.get('auth', {}).get('api_key')
    
    # Log the configuration (without sensitive data)
    logger.info(f"Using BASE_URL: {BASE_URL}")
    logger.info(f"Using PROJECT_NAME: {PROJECT_NAME}")
    logger.info(f"Using PROJECT_ID: {PROJECT_ID}")
    logger.info(f"Using GITHUB_REPO_PATH: {GITHUB_REPO_PATH}")
    logger.info(f"API_KEY is {'set' if API_KEY else 'not set'}")
    
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    logger.error("Using default configuration")
    BASE_URL = "https://test724810.a-vir-r1.int.ipaas.automation.ibm.com"
    PROJECT_NAME = "YOUR_PROJECT_NAME"
    PROJECT_ID = "YOUR_PROJECT_ID"
    GITHUB_REPO_PATH = "./github_repo"
    API_KEY = None

# Create main assets directory
ASSETS_DIR = os.path.join(GITHUB_REPO_PATH, "downloaded_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Create workflows directory inside downloaded_assets
WORKFLOWS_DIR = os.path.join(ASSETS_DIR, "workflows")
os.makedirs(WORKFLOWS_DIR, exist_ok=True)

# Create other asset directories
FLOWS_DIR = os.path.join(ASSETS_DIR, "flows")
LISTENERS_DIR = os.path.join(ASSETS_DIR, "listeners")
MESSAGING_DIR = os.path.join(ASSETS_DIR, "messaging")

os.makedirs(FLOWS_DIR, exist_ok=True)
os.makedirs(LISTENERS_DIR, exist_ok=True)
os.makedirs(MESSAGING_DIR, exist_ok=True)

def get_auth_headers():
    """
    Create authentication headers based on available credentials
    """
    headers = {}
    
    if API_KEY:
        # Use the correct header name required by the API
        headers['X-INSTANCE-API-KEY'] = API_KEY
    
    return headers

def get_assets():
    """
    Get the list of assets from webMethods.io Integration
    """
    if not BASE_URL or not PROJECT_NAME:
        logger.error("BASE_URL or PROJECT_NAME is not set")
        return None
        
    # Ensure BASE_URL doesn't end with a slash
    base_url = BASE_URL.rstrip('/') if BASE_URL else ""
    url = f"{base_url}/apis/v1/rest/projects/{PROJECT_NAME}/assets"
    headers = get_auth_headers()
    
    try:
        logger.info(f"Fetching assets from {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        assets = response.json()
        logger.info(f"Successfully retrieved assets")
        return assets["output"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching assets: {e}")
        return None

def download_workflow(workflow_id):
    """
    Download a workflow using its ID
    """
    if not BASE_URL or not PROJECT_ID:
        logger.error("BASE_URL or PROJECT_ID is not set")
        return None
        
    # Ensure BASE_URL doesn't end with a slash
    base_url = BASE_URL.rstrip('/') if BASE_URL else ""
    url = f"{base_url}/apis/v1/rest/projects/{PROJECT_ID}/workflows/{workflow_id}/export"
    headers = get_auth_headers()
    
    try:
        logger.info(f"Getting download link for workflow {workflow_id}")
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        download_info = response.json()["output"]
        download_link = download_info["download_link"]
        
        logger.info(f"Downloading workflow from {download_link}")
        download_response = requests.get(download_link)
        download_response.raise_for_status()
        
        # Extract filename from URL
        parsed_url = urlparse(download_link)
        path_parts = parsed_url.path.split('/')
        filename = path_parts[-2] if len(path_parts) >= 2 else workflow_id  # Get the filename part
        
        # Save the file to the workflows directory inside downloaded_assets
        filepath = f"{WORKFLOWS_DIR}/{workflow_id}.zip"
        with open(filepath, 'wb') as f:
            f.write(download_response.content)
        
        logger.info(f"Workflow saved to {filepath}")
        return filepath
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading workflow {workflow_id}: {e}")
        return None

def save_flow_info(flows):
    """
    Save flow information to GitHub
    """
    if not flows:
        logger.info("No flows to save")
        return
    
    filepath = f"{FLOWS_DIR}/flow_list.json"
    with open(filepath, 'w') as f:
        json.dump(flows, f, indent=2)
    
    logger.info(f"Flow information saved to {filepath}")

def save_listener_info(listeners):
    """
    Save listener information to GitHub
    """
    if not listeners:
        logger.info("No listeners to save")
        return
    
    filepath = f"{LISTENERS_DIR}/listener_list.json"
    with open(filepath, 'w') as f:
        json.dump(listeners, f, indent=2)
    
    logger.info(f"Listener information saved to {filepath}")

def save_messaging_info(messaging):
    """
    Save messaging information to GitHub
    """
    if not messaging:
        logger.info("No messaging to save")
        return
    
    filepath = f"{MESSAGING_DIR}/messaging_list.json"
    with open(filepath, 'w') as f:
        json.dump(messaging, f, indent=2)
    
    logger.info(f"Messaging information saved to {filepath}")

def main():
    """
    Main function to orchestrate the asset pulling process
    """
    logger.info("Starting webMethods.io Integration Asset Puller")
    
    # Step 1: Get the list of assets
    assets = get_assets()
    if not assets:
        logger.error("Failed to retrieve assets. Exiting.")
        return
    
    # Step 2: Process workflows
    workflows = assets.get("workflows", [])
    logger.info(f"Found {len(workflows)} workflows")
    for workflow_id in workflows:
        download_workflow(workflow_id)
        # Add a small delay to avoid overwhelming the server
        time.sleep(1)
    
    # Save other asset information
    save_flow_info(assets.get("flows", []))
    save_listener_info(assets.get("listener", []))
    save_messaging_info(assets.get("messaging", []))
    
    logger.info("Asset pulling completed successfully")

if __name__ == "__main__":
    main()

# Made with Bob