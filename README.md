# webMethods.io Integration Asset Puller

This script pulls assets from webMethods.io Integration project tenant and saves them to GitHub. It can be run locally or automated using GitHub Actions.

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository or download the files
2. Install required dependencies:

```bash
pip install requests
```

## Configuration

Edit the `config.json` file to set your webMethods.io Integration project details:

```json
{
  "base_url": "https://test724810.a-vir-r1.int.ipaas.automation.ibm.com",
  "project_name": "YOUR_PROJECT_NAME",
  "project_id": "YOUR_PROJECT_ID",
  "github_repo_path": "./github_repo",
  "auth": {
    "api_key": "YOUR_API_KEY"
  }
}
```

- `base_url`: The base URL of your webMethods.io Integration tenant
- `project_name`: The name of your project
- `project_id`: The ID of your project
- `github_repo_path`: Local path where files will be saved
- `auth.api_key`: Your API key for authentication (if required)

## Local Usage

Run the script:

```bash
python webmethods_asset_puller.py
```

Or use the provided shell script:

```bash
./run_asset_puller.sh
```

The script will:
1. Get the list of assets from the webMethods.io Integration project
2. Download all workflows and save them to the `github_repo/workflows` directory
3. Save information about flows, listeners, and messaging to their respective directories

## GitHub Actions Setup

This repository includes a GitHub Actions workflow that can automatically pull assets from webMethods.io Integration on a schedule or when manually triggered.

For detailed setup instructions, see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md).

### Quick Setup

1. Add the following secrets to your GitHub repository:
   - `WEBMETHODS_BASE_URL`
   - `WEBMETHODS_PROJECT_NAME`
   - `WEBMETHODS_PROJECT_ID`
   - `WEBMETHODS_API_KEY`

2. The workflow will run daily at midnight UTC and can also be triggered manually.

## Output Structure

```
github_repo/
├── workflows/
│   ├── workflow1.zip
│   ├── workflow2.zip
│   └── ...
├── flows/
│   └── flow_list.json
├── listeners/
│   └── listener_list.json
└── messaging/
    └── messaging_list.json
```

## Logging

The script logs its activities to both the console and a log file named `webmethods_asset_puller.log`.

## Testing

A test script is provided to verify the functionality using mock data:

```bash
python test_script.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.