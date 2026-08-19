"""
Google Sheets Configuration
===========================

Data source configuration untuk membaca dari Google Sheets
Bukan Excel files atau GitHub URLs

Author: RDO Analytics
Date: August 2026
"""

# Google Sheet ID (dari URL)
GOOGLE_SHEET_ID = "1iHX4K_i4Pc_jR8gHU3_W5HHF601SpG0L"

# Mapping data sources ke sheet/tab names
google_sheets_mapping = {
    'youtube_studio': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Raw Content Youtube Studio'
    },
    'youtube_scraping': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Scraping Youtube Juli 2026'
    },
    'portal': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Databse Portal'  # Note: typo dalam sheet
    },
    'socmed': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Database Facebook, Instagram, Tiktok, X'
    }
}

# Additional sheets untuk enrichment data (optional)
additional_sheets = {
    'recap_youtube': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Recap Youtube'
    },
    'source_revenue_youtube': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Source Revenue Youtube'
    },
    'competitor_youtube': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Summary Competitor Youtube'
    },
    'competitor_portal': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Competitor Portal - Similar Web'
    },
    'revenue_direct_sales_portal': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Revenue Direct Sales Portal'
    },
    'revenue_direct_sales_socmed': {
        'sheet_id': GOOGLE_SHEET_ID,
        'tab_name': 'Revenue Direct Sales Socmed'
    }
}

# File mapping untuk kompatibilitas dengan kode existing
file_mapping = google_sheets_mapping

if __name__ == "__main__":
    print("📊 Google Sheets Configuration")
    print(f"Sheet ID: {GOOGLE_SHEET_ID}")
    print("\nData sources:")
    for key, config in google_sheets_mapping.items():
        print(f"  ✓ {key}: {config['tab_name']}")
