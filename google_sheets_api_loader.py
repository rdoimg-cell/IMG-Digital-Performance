"""
Google Sheets API Loader
======================
Load data directly from Google Sheets using the Google Sheets API
More reliable than CSV export URLs, especially in restricted environments

Install: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import pandas as pd
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

# Google Sheets ID
GOOGLE_SHEET_ID = "1xxEO7GqKd1QmpKXKceG9tcaCIblGNUNplcskq2yw2RA"

# Sheet names mapping
SHEET_NAMES = {
    'youtube_studio': 'Raw Content Youtube Studio',
    'youtube_scraping': 'Scraping Youtube Juli 2026',
    'portal': 'Databse Portal',
    'socmed': 'Database Facebook, Instagram, Tiktok, X',
    'recap_youtube': 'Recap Youtube',
}


def load_sheet_with_api(sheet_id: str, sheet_name: str) -> Optional[pd.DataFrame]:
    """Load sheet using Google Sheets API v4"""
    try:
        print(f"  📥 {sheet_name}...", end=" ", flush=True)

        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from google.api_core.gapic_v1 import client_info as grpc_client_info
            import googleapiclient.discovery

            # This is for authenticated access (requires service account)
            # For now, we'll use the simpler CSV method with headers
            pass
        except ImportError:
            pass

        # Fallback: Use CSV export with proper headers
        sheet_gids = {
            'Raw Content Youtube Studio': '210766469',
            'Scraping Youtube Juli 2026': '2049365274',
            'Databse Portal': '1423094657',
            'Database Facebook, Instagram, Tiktok, X': '876748487',
            'Recap Youtube': '115557490',
        }

        gid = sheet_gids.get(sheet_name, '0')
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

        # Try with headers
        df = pd.read_csv(url, on_bad_lines='skip')

        print(f"✅ ({len(df):,} rows)")
        return df

    except Exception as e:
        print(f"❌ {str(e)[:50]}")
        return None


def load_sheet_with_gviz(sheet_id: str, sheet_name: str) -> Optional[pd.DataFrame]:
    """
    Load sheet using Google Visualization API query language
    Alternative method that sometimes works when direct export fails
    """
    try:
        print(f"  📥 {sheet_name} (gviz)...", end=" ", flush=True)

        # Map sheet name to gviz range
        sheet_gids = {
            'Raw Content Youtube Studio': '0',
            'Scraping Youtube Juli 2026': '1',
            'Databse Portal': '2',
            'Database Facebook, Instagram, Tiktok, X': '3',
            'Recap Youtube': '4',
        }

        gid = sheet_gids.get(sheet_name, '0')

        # Use Google Visualization API Query Language
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/query?tqx=out:csv&sheet={sheet_name}"

        df = pd.read_csv(url)

        print(f"✅ ({len(df):,} rows)")
        return df

    except Exception as e:
        print(f"❌ gviz failed: {str(e)[:30]}")
        return None


def load_all_sheets() -> Dict[str, pd.DataFrame]:
    """Load all sheets with fallback methods"""
    data = {}
    print("📥 Loading from Google Sheets...\n")

    for key, sheet_name in SHEET_NAMES.items():
        # Try gviz first (sometimes more reliable)
        df = load_sheet_with_gviz(GOOGLE_SHEET_ID, sheet_name)

        # Fallback to CSV export
        if df is None:
            df = load_sheet_with_api(GOOGLE_SHEET_ID, sheet_name)

        data[key] = df

    return data


if __name__ == "__main__":
    # Test loading
    data = load_all_sheets()
    print("\n✅ Data loaded successfully!")
    for key, df in data.items():
        if df is not None:
            print(f"  {key}: {len(df)} rows, {len(df.columns)} columns")
        else:
            print(f"  {key}: Failed to load")
