"""
Diagnostic Script - Test Data Loading Methods
==============================================
Run this to see which loading method works in your environment
"""

import sys

def test_simple_csv_export():
    """Test: Direct CSV export URLs"""
    print("\n" + "="*60)
    print("TEST 1: Simple CSV Export (Original Method)")
    print("="*60)

    try:
        from simple_sheets_loader import load_all_sheets
        print("Loading...")
        data = load_all_sheets()

        loaded_count = sum(1 for df in data.values() if df is not None)
        total_count = len(data)

        print(f"\n✅ SUCCESS: {loaded_count}/{total_count} sheets loaded")

        for key, df in data.items():
            if df is not None:
                print(f"   ✓ {key}: {len(df):,} rows")
            else:
                print(f"   ✗ {key}: Failed to load")

        return True

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_gviz_method():
    """Test: Google Visualization API Query"""
    print("\n" + "="*60)
    print("TEST 2: Google Visualization API (gviz)")
    print("="*60)

    try:
        from google_sheets_api_loader import load_all_sheets
        print("Loading...")
        data = load_all_sheets()

        loaded_count = sum(1 for df in data.values() if df is not None)
        total_count = len(data)

        print(f"\n✅ SUCCESS: {loaded_count}/{total_count} sheets loaded")

        for key, df in data.items():
            if df is not None:
                print(f"   ✓ {key}: {len(df):,} rows")
            else:
                print(f"   ✗ {key}: Failed to load")

        return True

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_github_method():
    """Test: GitHub CSV Files"""
    print("\n" + "="*60)
    print("TEST 3: GitHub CSV Files")
    print("="*60)

    try:
        from github_csv_loader import load_all_sheets
        print("Loading...")
        data = load_all_sheets()

        loaded_count = sum(1 for df in data.values() if df is not None)
        total_count = len(data)

        print(f"\n✅ SUCCESS: {loaded_count}/{total_count} sheets loaded")

        for key, df in data.items():
            if df is not None:
                print(f"   ✓ {key}: {len(df):,} rows")
            else:
                print(f"   ✗ {key}: Failed to load")

        return True

    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║  DATA LOADING METHOD DIAGNOSTIC                              ║
║  Testing which method works in your environment              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    results = {
        "CSV Export": test_simple_csv_export(),
        "gviz (API Query)": test_gviz_method(),
        "GitHub CSV": test_github_method(),
    }

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    for method, success in results.items():
        status = "✅ WORKS" if success else "❌ FAILED"
        print(f"{method:20} {status}")

    print("\n📋 RECOMMENDATIONS:")

    working_methods = [m for m, s in results.items() if s]

    if not working_methods:
        print("""
❌ None of the methods worked. This might be due to:
   1. Network restrictions (firewall/proxy)
   2. Google Sheet not properly shared
   3. Wrong Sheet ID or sheet names

Actions:
   • Verify Google Sheet is shared with "Anyone with link"
   • Check Sheet ID: 1xxEO7GqKd1QmpKXKceG9tcaCIblGNUNplcskq2yw2RA
   • Verify sheet names match exactly
   • Check your internet connection
        """)

    elif "GitHub CSV" in working_methods:
        print("""
✅ GitHub CSV method works!

   Next steps:
   1. Export data as CSV from your Google Sheets
   2. Upload CSV files to GitHub repo
   3. Update streamlit_app.py to use github_csv_loader.py
   4. Deploy to Streamlit
        """)

    elif "gviz (API Query)" in working_methods:
        print("""
✅ Google Visualization API (gviz) works!

   You're all set!
   • Latest streamlit_app.py already uses this method
   • Deploy updated code to Streamlit
   • It should work without any changes
        """)

    elif "CSV Export" in working_methods:
        print("""
✅ Simple CSV Export works!

   No changes needed!
   • Your current method is working
   • Just deploy the code to Streamlit
        """)

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
