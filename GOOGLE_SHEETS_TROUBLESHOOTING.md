# Google Sheets Integration - Troubleshooting & Solutions

## Problem: 403 Forbidden Error

When loading data from Google Sheets CSV export URLs, you may see:
```
Tunnel connection failed: 403 Forbidden
```

This happens because:
- **Streamlit Cloud** has network restrictions that block direct CSV export URLs
- Google Sheets CSV export may require authentication for some configurations
- The environment may be behind a proxy/firewall that blocks Google domains

## Solution Options

### ✅ Option 1: Use Google Visualization API Query (RECOMMENDED FIRST)

**Status**: More reliable than CSV export, no authentication needed

The `google_sheets_api_loader.py` includes a **gviz** method that often works when direct CSV export fails.

**How it works**:
- Uses Google's Visualization API Query Language
- Works with publicly shared Google Sheets
- No authentication required
- More resilient than CSV export

**To use it**:

1. **Update streamlit_app.py** (already done in latest version)
   - App now automatically tries gviz method first
   - Falls back to CSV export if needed

2. **Ensure your Google Sheet is shared**:
   - Open your Google Sheet
   - Click "Share" button
   - Set to "Anyone with the link can view" (you have this already ✓)

3. **Deploy to Streamlit**:
   - Push updated code to GitHub
   - Streamlit should auto-redeploy
   - Check app logs for which method is being used

### 🟡 Option 2: Use GitHub CSV Files (MOST RELIABLE)

**Status**: Guaranteed to work, requires one-time setup

If Google Sheets methods continue to fail, this is the most reliable approach.

**How it works**:
1. Export data as CSV from Google Sheets
2. Upload CSV files to GitHub
3. App loads from GitHub (no 403 errors, proven to work)

**Setup steps**:

#### Step 1: Export Data from Google Sheets as CSV

For each sheet tab:
1. Open your Google Sheet
2. Select the sheet tab (e.g., "Raw Content Youtube Studio")
3. File → Download → Comma Separated Values (.csv)
4. Save as: `youtube_studio.csv`

Repeat for:
- `youtube_scraping.csv` (from "Scraping Youtube Juli 2026")
- `portal.csv` (from "Databse Portal")
- `socmed.csv` (from "Database Facebook, Instagram, Tiktok, X")
- `recap_youtube.csv` (from "Recap Youtube") - optional but recommended

#### Step 2: Upload to GitHub

1. Go to your GitHub repository (the one with your code)
2. Click "Add file" → "Upload files"
3. Drag and drop the CSV files
4. Commit with message: "Add data CSV files"

#### Step 3: Update Streamlit App

Create or update `github_csv_loader.py` with your GitHub info:

```python
GITHUB_OWNER = "mncgroup"      # Your GitHub username
GITHUB_REPO = "analytics-data" # Your repository name
GITHUB_BRANCH = "main"
```

Update `streamlit_app.py`:

```python
@st.cache_resource
def load_chatbot_data():
    """Load data from GitHub CSV files"""
    try:
        from github_csv_loader import load_all_sheets
        
        data = load_all_sheets()
        
        bot = AnalyticsBot()
        bot.db.studio_data = data.get('youtube_studio')
        bot.db.scraping_data = data.get('youtube_scraping')
        bot.db.portal_data = data.get('portal')
        bot.db.socmed_data = data.get('socmed')
        
        return bot, True, None
    except Exception as e:
        return None, False, str(e)
```

#### Step 4: Deploy

Push to GitHub and Streamlit will auto-redeploy.

**Updating data**:
- Each week when data updates, export CSVs from Google Sheets
- Upload to GitHub repo (replace existing files)
- Streamlit automatically reloads the new data

### 🔵 Option 3: Use Google Sheets API (ADVANCED)

**Status**: Most powerful, requires setup

If you need real-time data without manual exports:

1. **Create Google Cloud Service Account**:
   - Go to https://console.cloud.google.com/
   - Create new project
   - Create service account
   - Download JSON key

2. **Share Google Sheet with service account**:
   - Copy service account email (from JSON key)
   - Open Google Sheet
   - Click Share, paste email, give Editor access

3. **Update requirements.txt**:
   ```
   google-auth-oauthlib
   google-auth-httplib2
   google-api-python-client
   ```

4. **Update loader code** to use service account JSON

---

## Recommended Path

**For quick fix**: Try Option 1 (gviz) - already implemented
- Simplest, no changes needed
- Works for most Google Sheets configurations
- Test: Deploy and check logs

**If Option 1 fails**: Use Option 2 (GitHub CSV)
- Most reliable, proven to work
- Requires exporting CSVs weekly
- No authentication headaches

**For enterprise setup**: Use Option 3 (API)
- Requires more setup
- Real-time data updates
- Most flexible

---

## Testing

To test which method works:

```bash
# Test gviz method
python google_sheets_api_loader.py

# Test GitHub method (after setup)
python github_csv_loader.py
```

Check output to see which one succeeds ✅

---

## Checklist

- [ ] Google Sheet is shared with "Anyone with the link can view"
- [ ] Sheet tab names match exactly in code:
  - [ ] `Raw Content Youtube Studio`
  - [ ] `Scraping Youtube Juli 2026`
  - [ ] `Databse Portal` (note the typo!)
  - [ ] `Database Facebook, Instagram, Tiktok, X`
  - [ ] `Recap Youtube`
- [ ] Google Sheet ID is correct in code: `1xxEO7GqKd1QmpKXKceG9tcaCIblGNUNplcskq2yw2RA`
- [ ] Latest code deployed to Streamlit
- [ ] Check Streamlit app logs for loading status

---

## Questions?

If you choose **Option 2 (GitHub CSV)** and need help:
1. Export the CSV files from your Google Sheet
2. Tell me and I'll guide you uploading to GitHub
3. I'll update your Streamlit app code

For **Option 1 (gviz)**: Just deploy latest code and check if it works!
