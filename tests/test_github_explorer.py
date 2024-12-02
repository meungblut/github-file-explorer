import os
import pytest
from github_explorer.commands import FindExcelFilesCommand, DownloadExcelFilesCommand, GithubClient

@pytest.mark.integration
def test_find_excel_files_command():
    # Note: Replace with an actual test org you have access to
    org_name = 'test-org'
    client = GithubClient()
    
    find_command = FindExcelFilesCommand(org_name)
    excel_files = client.execute_command(find_command)
    
    assert isinstance(excel_files, list)

@pytest.mark.integration
def test_download_excel_files_command():
    # Note: Replace with an actual test org you have access to
    org_name = 'test-org'
    output_dir = 'test_excel_downloads'
    
    client = GithubClient()
    download_command = DownloadExcelFilesCommand(org_name, output_dir)
    
    downloaded_files = client.execute_command(download_command)
    
    assert len(downloaded_files) > 0
    assert all(os.path.exists(file) for file in downloaded_files)

@pytest.mark.unit
def test_token_retrieval_mock():
    from unittest.mock import patch
    from github_explorer.config import TokenRetriever
    
    with patch.dict(os.environ, {'GITHUB_PAT': 'test-token'}):
        assert TokenRetriever.get_pat() == 'test-token'
