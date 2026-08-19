"""
GitHub CSV Loader
=================
Load data from CSV files stored on GitHub
Most reliable method - no 403 errors, no authentication needed
"""

import pandas as pd
from typing import Dict, Optional

# GitHub repository configuration
GITHUB_OWNER = "mncgroup"  # Change to your GitHub username
GITHUB_REPO = "analytics-data"  # Change to your repository name
GITHUB_BRANCH = "main"

# CSV file mappings
CSV_FILES = {
    'youtube_studio': 'youtube_studio.csv',
    'youtube_scraping': 'youtube_scraping.csv',
    'portal': 'portal.csv',
    'socmed': 'socmed.csv',
    'recap_youtube': 'recap_youtube.csv',
}


def get_github_raw_url(owner: str, repo: str, branch: str, filename: str) -> str:
    """Generate GitHub raw content URL"""
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filename}"


def load_sheet_from_github(owner: str, repo: str, branch: str, filename: str) -> Optional[pd.DataFrame]:
    """Load CSV file from GitHub"""
    try:
        sheet_name = filename.replace('.csv', '').replace('_', ' ').title()
        print(f"  📥 {sheet_name}...", end=" ", flush=True)

        url = get_github_raw_url(owner, repo, branch, filename)
        df = pd.read_csv(url)

        print(f"✅ ({len(df):,} rows)")
        return df

    except Exception as e:
        print(f"❌ {str(e)[:50]}")
        return None


def load_all_sheets_from_github(owner: str = GITHUB_OWNER,
                               repo: str = GITHUB_REPO,
                               branch: str = GITHUB_BRANCH) -> Dict[str, pd.DataFrame]:
    """Load all CSV files from GitHub"""
    data = {}
    print("📥 Loading from GitHub...\n")

    for key, filename in CSV_FILES.items():
        df = load_sheet_from_github(owner, repo, branch, filename)
        data[key] = df

    return data


# For direct use with updated GitHub configuration
def load_all_sheets() -> Dict[str, pd.DataFrame]:
    """Load all sheets from GitHub (uses configured repository)"""
    return load_all_sheets_from_github()


if __name__ == "__main__":
    print("🔧 GitHub CSV Loader Configuration")
    print(f"   Owner: {GITHUB_OWNER}")
    print(f"   Repo: {GITHUB_REPO}")
    print(f"   Branch: {GITHUB_BRANCH}")
    print("\n📝 To use this loader:")
    print("   1. Update GITHUB_OWNER and GITHUB_REPO in this file")
    print("   2. Upload CSV files to GitHub repository")
    print("   3. Import load_all_sheets() in streamlit_app.py")
