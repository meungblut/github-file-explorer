# GitHub File Explorer

## Overview
A Python tool to explore and download Excel files from GitHub organizations using GraphQL and Command patterns.

## Features
- Retrieve GitHub Personal Access Token via environment or file
- Find Excel files in an organization
- Download Excel files from repositories

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Set your GitHub PAT via:
1. Environment variable: `GITHUB_PAT`
2. `.github_pat` file in the project root

## Usage
```python
from github_explorer.commands import GithubClient, FindExcelFilesCommand, DownloadExcelFilesCommand

client = GithubClient()

# Find Excel files
find_command = FindExcelFilesCommand('your-org-name')
excel_files = client.execute_command(find_command)

# Download Excel files
download_command = DownloadExcelFilesCommand('your-org-name')
downloaded_files = client.execute_command(download_command)
```