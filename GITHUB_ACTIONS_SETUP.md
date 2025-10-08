# Setting Up GitHub Actions for webMethods.io Asset Puller

This guide explains how to set up GitHub Actions to automatically pull assets from webMethods.io Integration and save them to your GitHub repository.

## Prerequisites

1. A GitHub repository where you want to store your webMethods.io assets
2. Access to webMethods.io Integration with appropriate API permissions
3. Your webMethods.io project name and ID

## Setup Steps

### 1. Add GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click on "New repository secret"
4. Add the following secrets:

   - `WEBMETHODS_BASE_URL`: The base URL of your webMethods.io Integration tenant (e.g., `https://test724810.a-vir-r1.int.ipaas.automation.ibm.com`)
   - `WEBMETHODS_PROJECT_NAME`: Your project name
   - `WEBMETHODS_PROJECT_ID`: Your project ID
   - `WEBMETHODS_API_KEY`: Your API key for authentication
   - `GH_PAT`: A GitHub Personal Access Token with repo scope (required for pushing changes)

### 2. Create a Personal Access Token (PAT)

To allow GitHub Actions to push changes to your repository, you need to create a Personal Access Token:

1. Go to your GitHub account settings
2. Click on "Developer settings" > "Personal access tokens" > "Tokens (classic)"
3. Click on "Generate new token" > "Generate new token (classic)"
4. Give it a descriptive name like "WebMethods Asset Puller"
5. Select the "repo" scope to allow pushing to repositories
6. Click "Generate token"
7. Copy the token and add it as a secret named `GH_PAT` in your repository

### 2. GitHub Actions Workflow

The GitHub Actions workflow is already set up in `.github/workflows/webmethods_asset_puller.yml`. This workflow:

- Runs automatically every day at midnight UTC
- Can be triggered manually with different environment options
- Pulls assets from webMethods.io Integration
- Commits and pushes the changes to your repository

### 3. Manual Trigger

To manually trigger the workflow:

1. Go to your GitHub repository
2. Click on "Actions"
3. Select "WebMethods.io Asset Puller" from the workflows list
4. Click on "Run workflow"
5. Select the environment (test, dev, or prod)
6. Click "Run workflow"

### 4. Customizing the Schedule

If you want to change the schedule, edit the `.github/workflows/webmethods_asset_puller.yml` file:

```yaml
on:
  schedule:
    # This runs at midnight UTC every day
    # Change this to your preferred schedule using cron syntax
    - cron: '0 0 * * *'
```

Common cron schedule examples:
- `0 0 * * *`: Daily at midnight UTC
- `0 0 * * 1-5`: Weekdays at midnight UTC
- `0 0 1 * *`: Monthly on the 1st at midnight UTC
- `0 */6 * * *`: Every 6 hours

### 5. Viewing Results

After the workflow runs:

1. Go to your GitHub repository
2. Click on "Actions"
3. Click on the latest "WebMethods.io Asset Puller" workflow run
4. View the logs to see what assets were pulled
5. Check the commit history to see the changes made to your repository

## Troubleshooting

If the workflow fails:

1. Check the workflow run logs for error messages
2. Verify that your secrets are correctly set up
3. Ensure your API key has the necessary permissions
4. Check that your webMethods.io Integration tenant is accessible

## Security Considerations

- Never commit API keys or credentials directly to your repository
- Use GitHub Secrets for all sensitive information
- Consider using a dedicated service account with limited permissions for the API access