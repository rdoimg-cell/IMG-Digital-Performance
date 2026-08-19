"""
Simple Google Sheets Loader
===========================
Read Google Sheets menggunakan CSV export - TANPA gspread dependency
"""

import pandas as pd
from typing import Dict, Optional

GOOGLE_SHEET_ID = "1xxEO7GqKd1QmpKXKceG9tcaCIblGNUNplcskq2yw2RA"


def get_sheet_csv_url(sheet_id: str, sheet_name: str) -> str:
    """Generate CSV export URL untuk specific sheet tab"""
    # Mapping sheet names ke GIDs (kamu bisa cek dari URL)
    sheet_gids = {
        'Raw Content Youtube Studio': '0',  # Default tab usually 0
        'Scraping Youtube Juli 2026': '1',
        'Databse Portal': '2',
        'Database Facebook, Instagram, Tiktok, X': '3',
    }

    gid = sheet_gids.get(sheet_name, '0')
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return url


def load_sheet(sheet_id: str, sheet_name: str) -> Optional[pd.DataFrame]:
    """Load sheet by name using CSV export"""
    try:
        print(f"  📥 {sheet_name}...", end=" ", flush=True)

        url = get_sheet_csv_url(sheet_id, sheet_name)
        df = pd.read_csv(url)

        print(f"✅ ({len(df):,} rows)")
        return df

    except Exception as e:
        print(f"❌ {str(e)[:50]}")
        return None


def load_all_sheets() -> Dict[str, pd.DataFrame]:
    """Load semua sheet yang diperlukan"""
    sheets = {
        'youtube_studio': 'Raw Content Youtube Studio',
        'youtube_scraping': 'Scraping Youtube Juli 2026',
        'portal': 'Databse Portal',
        'socmed': 'Database Facebook, Instagram, Tiktok, X',
    }

    data = {}
    print("📥 Loading from Google Sheets...\n")

    for key, sheet_name in sheets.items():
        df = load_sheet(GOOGLE_SHEET_ID, sheet_name)
        data[key] = df

    return data
