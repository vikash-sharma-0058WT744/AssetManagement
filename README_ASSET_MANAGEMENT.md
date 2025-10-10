# webMethods.io Asset Management

This repository contains scripts and workflows for managing webMethods.io Integration assets.

## Overview

The asset management system allows you to:

1. Download assets from webMethods.io Integration projects
2. Store them in a structured folder hierarchy
3. Track changes over time using Git

## Directory Structure

```
/
├── downloaded_assets/       # Main directory for all downloaded assets
│   ├── workflows/           # Contains workflow ZIP files
│   ├── flows/               # Contains flow service information
│   ├── listeners/           # Contains listener information
│   └── messaging/           # Contains messaging information
├── config.json              # Configuration file
└── modified_webmethods_asset_puller.py  # Asset download script
```

## Configuration

The `config.json` file contains the following settings:

```json
{
  "base_url": "https://your-webmethods-instance.com",
  "project_name": "YourProjectName",
  "project_id": "your-project-id",
  "github_repo_path": "./github_repo",
  "auth": {
    "api_key": "YOUR_API_KEY_HERE"
  }
}
```

## GitHub Actions Workflow

The GitHub Actions workflow (`modified_webmethods_asset_puller.yml`) automatically:

1. Runs on a schedule (daily at midnight UTC)
2. Downloads the latest assets from your webMethods.io Integration project
3. Commits and pushes the changes to your repository

## Manual Usage

To run the asset puller manually:

```bash
# Make sure the script is executable
chmod +x modified_webmethods_asset_puller.py

# Run the script
./modified_webmethods_asset_puller.py
```

## Testing

To run the tests:

```bash
# Make the test script executable
chmod +x run_tests.sh

# Run the tests
./run_tests.sh
```

## Customization

You can customize the asset puller by:

1. Modifying the `config.json` file
2. Updating the GitHub Actions workflow schedule
3. Adding additional asset types to the script

## Troubleshooting

If you encounter issues:

1. Check the log file (`webmethods_asset_puller.log`)
2. Verify your API key and project settings
3. Ensure your GitHub repository has the necessary secrets configured