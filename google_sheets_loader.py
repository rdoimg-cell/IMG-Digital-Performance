"""
Google Sheets Data Loader
=========================

Load data dari Google Sheets (public sheets)
Supports multiple tabs dalam satu spreadsheet

Author: RDO Analytics
Date: August 2026
"""

import pandas as pd
import gspread
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsLoader:
    """Load data dari Google Sheets public"""

    @staticmethod
    def load_from_google_sheets(sheet_config: Dict) -> Optional[pd.DataFrame]:
        """
        Load data dari Google Sheet by tab name

        Args:
            sheet_config: Dict dengan 'sheet_id' dan 'tab_name'

        Returns:
            DataFrame atau None jika gagal
        """
        try:
            sheet_id = sheet_config.get('sheet_id')
            tab_name = sheet_config.get('tab_name')

            if not sheet_id or not tab_name:
                logger.error("Missing sheet_id or tab_name in config")
                return None

            # Authorize dengan public access (no auth needed for public sheets)
            gc = gspread.Sheets(sheet_id)

            # Open spreadsheet by ID
            sh = gc.open_by_key(sheet_id)

            # Get worksheet by name
            worksheet = sh.worksheet(tab_name)

            # Get all values
            data = worksheet.get_all_values()

            if not data:
                logger.warning(f"No data in {tab_name}")
                return None

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])  # First row is header

            logger.info(f"✓ Loaded {len(df)} records from '{tab_name}'")
            return df

        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"Worksheet '{tab_name}' not found in sheet {sheet_id}")
            return None
        except Exception as e:
            logger.error(f"Error loading from Google Sheets: {str(e)}")
            return None

    @staticmethod
    def load_from_file_mapping(file_mapping: Dict[str, Dict]) -> Dict[str, pd.DataFrame]:
        """
        Load multiple sheets from Google Sheets

        Args:
            file_mapping: Dict dengan config untuk setiap data source

        Returns:
            Dict dengan loaded dataframes
        """
        data = {}

        for key, config in file_mapping.items():
            try:
                print(f"📥 Loading {key}...", end=" ", flush=True)
                df = GoogleSheetsLoader.load_from_google_sheets(config)

                if df is not None:
                    data[key] = df
                    print(f"✅ ({len(df):,} rows)")
                else:
                    print("❌ Failed")
                    data[key] = None

            except Exception as e:
                print(f"❌ {str(e)[:50]}")
                data[key] = None

        return data


if __name__ == "__main__":
    from google_sheets_config import google_sheets_mapping

    print("Testing Google Sheets Loader...")
    data = GoogleSheetsLoader.load_from_file_mapping(google_sheets_mapping)

    print("\n📊 Summary:")
    for key, df in data.items():
        if df is not None:
            print(f"  ✓ {key}: {len(df)} rows, {len(df.columns)} columns")
        else:
            print(f"  ✗ {key}: Failed")
