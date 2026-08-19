"""
Data Loading Module - Support for Local and GitHub Sources
===========================================================

Handles loading data from:
- Local Excel files
- GitHub raw URLs (public repositories)
- GitHub with authentication tokens (private repositories)

Author: RDO Analytics
Date: August 2026
"""

import pandas as pd
import logging
import tempfile
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DataLoader:
    """Load data from various sources"""

    @staticmethod
    def load_from_file_mapping(file_mapping: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        """
        Load data from file mapping (supports local files and GitHub URLs)

        Args:
            file_mapping: Dict with keys (youtube_studio, youtube_scraping, portal, socmed)
                         Values can be local paths or GitHub URLs

        Returns:
            Dict with loaded dataframes or None if failed
        """
        data = {
            'youtube_studio': None,
            'youtube_scraping': None,
            'portal': None,
            'socmed': None
        }

        sheet_names = {
            'youtube_studio': 'Content Youtube Studio',
            'youtube_scraping': 'Scraping Juli 2026',
            'portal': 'Monthly Portal IMG',
            'socmed': 'Facebook, Instagram, Tiktok, X'
        }

        for key, file_path in file_mapping.items():
            if file_path and key in sheet_names:
                try:
                    print(f"📥 Loading {key}...", end=" ", flush=True)

                    if file_path.startswith('http'):
                        # GitHub URL
                        df = DataLoader.load_from_github(file_path, sheet_names[key])
                    else:
                        # Local file
                        df = DataLoader.load_from_local(file_path, sheet_names[key])

                    if df is not None:
                        data[key] = df
                        print(f"✓ ({len(df):,} rows)")
                    else:
                        print("✗ Failed")

                except Exception as e:
                    error_detail = str(e)
                    print(f"✗ Error: {error_detail[:100]}")
                    logger.error(f"Error loading {key}: {error_detail}")
                    logger.error(f"File path: {file_path}")

        return data

    @staticmethod
    def load_from_local(file_path: str, sheet_name: str) -> Optional[pd.DataFrame]:
        """Load data from local Excel file"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error loading local file {file_path}: {str(e)}")
            return None

    @staticmethod
    def load_from_github(url: str, sheet_name: str) -> Optional[pd.DataFrame]:
        """
        Load data from GitHub raw URL

        Args:
            url: GitHub raw URL (with or without token)
            sheet_name: Excel sheet name

        Returns:
            DataFrame or None if failed
        """
        try:
            # Try with requests first (better error handling)
            try:
                import requests
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                # Save to temp file
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name

                # Load from temp
                df = pd.read_excel(tmp_path, sheet_name=sheet_name)
                os.unlink(tmp_path)

                logger.info(f"Loaded {len(df)} records from GitHub: {url[:80]}...")
                return df

            except ImportError:
                # Fallback: use pandas directly (less error info)
                logger.warning("requests module not available, using pandas URL reading")
                df = pd.read_excel(url, sheet_name=sheet_name)
                return df

        except Exception as e:
            logger.error(f"Error loading from GitHub {url}: {str(e)}")
            return None

    @staticmethod
    def validate_data(data: Dict[str, pd.DataFrame]) -> bool:
        """
        Validate loaded data

        Returns:
            True if data is valid, False otherwise
        """
        valid = False

        # Check if at least one dataset loaded
        for key, df in data.items():
            if df is not None and len(df) > 0:
                valid = True
                logger.info(f"✓ {key}: {len(df)} records")
            else:
                logger.warning(f"✗ {key}: No data")

        return valid


def load_data_with_fallback(
    primary_mapping: Dict[str, str],
    fallback_mapping: Optional[Dict[str, str]] = None
) -> Dict[str, pd.DataFrame]:
    """
    Load data with fallback

    Try primary mapping (e.g., GitHub URLs).
    If fails, try fallback mapping (e.g., local files).

    Args:
        primary_mapping: Primary source mapping
        fallback_mapping: Fallback mapping if primary fails

    Returns:
        Loaded data dictionary
    """
    print("📊 Loading data...")

    # Try primary
    data = DataLoader.load_from_file_mapping(primary_mapping)

    # Check if successful
    if DataLoader.validate_data(data):
        return data

    # Fallback
    if fallback_mapping:
        print("\n⚠️  Primary source failed, trying fallback...")
        data = DataLoader.load_from_file_mapping(fallback_mapping)

    return data


if __name__ == "__main__":
    # Example usage
    from github_config import github_file_mapping, local_file_mapping

    # Load with fallback
    data = load_data_with_fallback(github_file_mapping, local_file_mapping)

    # Print summary
    print("\n📊 Data Summary:")
    for key, df in data.items():
        if df is not None:
            print(f"  {key}: {len(df):,} rows")
        else:
            print(f"  {key}: No data")
