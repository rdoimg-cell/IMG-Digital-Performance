"""
GitHub Data Source Configuration
=================================

Use this file to configure chatbot to fetch data from GitHub instead of local files.

How to use:
1. Create GitHub repo and upload your Excel files
2. Get raw URLs from GitHub (instructions in GITHUB_SETUP.md)
3. Replace YOUR_USERNAME with your GitHub username
4. Run: from github_config import file_mapping
5. Pass to chatbot: bot.load_data(file_mapping)

Author: RDO Analytics
Date: August 2026
"""

# ============================================
# OPTION 1: USE GITHUB (Recommended)
# ============================================
# Replace YOUR_USERNAME with your actual GitHub username
# Example: "https://raw.githubusercontent.com/rdo-analytics/mnc-analytics-data/main/..."

github_file_mapping = {
    'youtube_studio': 'https://raw.githubusercontent.com/rdoimg-cell/IMG-Digital-Performance/main/Database%20Konten%20IMG%20Juli%202026.xlsx',
    'youtube_scraping': 'https://raw.githubusercontent.com/rdoimg-cell/IMG-Digital-Performance/main/Database%20Konten%20Scraping%20Juli%202026.xlsx',
    'portal': 'https://raw.githubusercontent.com/rdoimg-cell/IMG-Digital-Performance/main/Database%20Portal%20Performance%20IMG%202026.xlsx',
    'socmed': 'https://raw.githubusercontent.com/rdoimg-cell/IMG-Digital-Performance/main/Database%20Rekap%20Socmed%20IMG%202026.xlsx'
}

# ============================================
# OPTION 2: USE LOCAL FILES (Fallback)
# ============================================
# Use this if GitHub is not available

local_file_mapping = {
    'youtube_studio': './data/Database_Konten_IMG_Juli_2026.xlsx',
    'youtube_scraping': './data/Database_Konten_Scraping_Juli_2026.xlsx',
    'portal': './data/Database_Portal_Performance_IMG_2026.xlsx',
    'socmed': './data/Database_Rekap_Socmed_IMG_2026.xlsx'
}

# ============================================
# OPTION 3: MIXED (GitHub + Local Fallback)
# ============================================
# Try GitHub first, fall back to local if unavailable

mixed_file_mapping = {
    'youtube_studio': ['https://raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Konten_IMG_Juli_2026.xlsx',
                       './data/Database_Konten_IMG_Juli_2026.xlsx'],
    'youtube_scraping': ['https://raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Konten_Scraping_Juli_2026.xlsx',
                         './data/Database_Konten_Scraping_Juli_2026.xlsx'],
    'portal': ['https://raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Portal_Performance_IMG_2026.xlsx',
               './data/Database_Portal_Performance_IMG_2026.xlsx'],
    'socmed': ['https://raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Rekap_Socmed_IMG_2026.xlsx',
               './data/Database_Rekap_Socmed_IMG_2026.xlsx']
}

# ============================================
# PRIVATE REPOSITORY? (With GitHub Token)
# ============================================
# For private repos, use Personal Access Token:
# 1. Create token: https://github.com/settings/tokens
# 2. Select 'repo' scope
# 3. Copy token
# 4. Use format: https://TOKEN@raw.githubusercontent.com/USERNAME/REPO/main/FILE.xlsx

private_repo_file_mapping = {
    'youtube_studio': 'https://YOUR_TOKEN@raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Konten_IMG_Juli_2026.xlsx',
    'youtube_scraping': 'https://YOUR_TOKEN@raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Konten_Scraping_Juli_2026.xlsx',
    'portal': 'https://YOUR_TOKEN@raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Portal_Performance_IMG_2026.xlsx',
    'socmed': 'https://YOUR_TOKEN@raw.githubusercontent.com/YOUR_USERNAME/mnc-analytics-data/main/Database_Rekap_Socmed_IMG_2026.xlsx'
}

# ============================================
# SELECT WHICH CONFIG TO USE
# ============================================
# Change this variable to switch between configurations

# file_mapping = local_file_mapping           # Use local files
file_mapping = github_file_mapping             # Use GitHub (default)
# file_mapping = mixed_file_mapping           # GitHub + local fallback
# file_mapping = private_repo_file_mapping    # Private repo with token

# ============================================
# QUICK START INSTRUCTIONS
# ============================================

QUICK_START = """
🚀 GITHUB DATA SOURCE - QUICK START

Step 1: Create GitHub Repo
   → Go to https://github.com/new
   → Name: mnc-analytics-data
   → Add README
   → Create

Step 2: Upload Excel Files
   → Click "Add file" > "Upload files"
   → Drag & drop your 4 Excel files
   → Commit changes

Step 3: Get Raw URLs
   → Click each file
   → Click "Raw" button
   → Copy URL

Step 4: Update This File
   → Replace YOUR_USERNAME with your GitHub username
   → Replace URLs with your raw URLs
   → Change line: file_mapping = github_file_mapping

Step 5: Test
   → python3 chatbot_demo.py
   → Ask: "Channel mana paling profitable?"
   → Should work! 🎉

Full instructions: GITHUB_SETUP.md
"""

if __name__ == "__main__":
    print(QUICK_START)
