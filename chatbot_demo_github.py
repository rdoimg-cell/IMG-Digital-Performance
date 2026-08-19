#!/usr/bin/env python3
"""
MNC Analytics Chatbot - Interactive Demo (GitHub Version)
===========================================================
CLI interface untuk testing chatbot dengan data dari GitHub

Usage:
    python3 chatbot_demo_github.py

Atau gunakan dengan local files:
    python3 chatbot_demo_github.py --local

Author: RDO Analytics Team
Created: August 2026
"""

import sys
import os
import logging
import argparse
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_system import AnalyticsBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('./logs/chatbot_demo.log')
    ]
)
logger = logging.getLogger(__name__)


class ChatbotDemo:
    """Interactive chatbot demo interface with GitHub support"""

    def __init__(self, use_github=True):
        self.bot = AnalyticsBot()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.use_github = use_github

    def load_data(self):
        """Load data from GitHub or local files"""

        if self.use_github:
            # Import config for GitHub URLs
            try:
                from github_config import file_mapping as github_mapping
                file_mapping = github_mapping
                print("\n✓ Using GitHub data source")
            except ImportError:
                print("\n⚠️  github_config not found, falling back to local files")
                file_mapping = self.get_local_mapping()
        else:
            file_mapping = self.get_local_mapping()
            print("\n✓ Using local data files")

        print("📊 Loading data...", end=" ", flush=True)
        try:
            success = self.bot.load_data(file_mapping)
            if success:
                print("✓ Data loaded successfully!\n")
                logger.info(f"Data loaded from {'GitHub' if self.use_github else 'local files'}")
                return True
            else:
                print("✗ Failed to load data")
                logger.error("Data loading failed")
                return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            logger.error(f"Data loading error: {str(e)}")
            return False

    @staticmethod
    def get_local_mapping():
        """Get local file mapping"""
        return {
            'youtube_studio': './data/Database_Konten_IMG_Juli_2026.xlsx',
            'youtube_scraping': './data/Database_Konten_Scraping_Juli_2026.xlsx',
            'portal': './data/Database_Portal_Performance_IMG_2026.xlsx',
            'socmed': './data/Database_Rekap_Socmed_IMG_2026.xlsx'
        }

    def startup(self):
        """Display startup message"""
        print("\n" + "=" * 70)
        print("  🤖 MNC ANALYTICS CHATBOT - INTERACTIVE DEMO")
        print("  " + "=" * 66)
        print("  📊 Chatbot Analytics System v1.0.0")
        print("  🚀 Powered by Natural Language Processing")
        print("=" * 70)

    def display_help(self):
        """Display help information"""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║                      CHATBOT HELP & EXAMPLES                   ║
╚════════════════════════════════════════════════════════════════╝

📚 AVAILABLE COMMANDS:
  help      - Show this help message
  history   - Show conversation history
  clear     - Clear conversation history
  exit      - Exit chatbot

🎯 EXAMPLE QUESTIONS (Try These!):

  Performance Comparison:
  → "Bagaimana performa IMG vs kompetitor di 2026?"
  → "Channel IMG mana yang terbaik?"

  Revenue Analysis:
  → "Channel mana yang paling profitable?"
  → "Berapa total revenue IMG?"

  Trend Analysis:
  → "Bagaimana trend engagement terbaru?"
  → "Growth rate bulan ini vs bulan lalu?"

  Top Performers:
  → "Top 5 channel dengan views terbanyak?"
  → "Channel mana yang paling sukses?"

  Cluster Comparison:
  → "Cluster iNews vs KompasTV, siapa unggul?"
  → "Bagaimana performa Sindonews vs MetroTV?"

  Engagement Analysis:
  → "Berapa engagement rate rata-rata?"
  → "Channel mana dengan engagement tertinggi?"

  Competitive Analysis:
  → "Siapa kompetitor terberat kami?"
  → "Market share IMG berapa persen?"

💡 TIPS FOR BETTER RESULTS:
  • Be specific: mention channel, metric, or time period
  • Use keywords: revenue, engagement, views, trend
  • Compare for richer insights
  • One question at a time

🔄 SPECIAL COMMANDS IN CHAT:
  Type 'help'    → Show this message
  Type 'history' → Show past questions
  Type 'clear'   → Clear chat history
  Type 'exit'    → Quit chatbot

═══════════════════════════════════════════════════════════════════
"""
        print(help_text)

    def display_history(self):
        """Display conversation history"""
        if not self.bot.conversation_history:
            print("\n📝 No conversation history yet.")
            return

        print("\n" + "=" * 70)
        print("  📋 CONVERSATION HISTORY")
        print("=" * 70)

        for i, entry in enumerate(self.bot.conversation_history[-10:], 1):
            print(f"\n  [{i}] {entry.get('timestamp', 'N/A')}")
            print(f"      Q: {entry.get('user_question', 'N/A')[:60]}...")
            print(f"      Type: {entry.get('analysis_type', 'N/A')}")

    def display_response(self, response):
        """Display formatted response"""
        print("\n📈 Analytics Bot:")
        print("─" * 70)
        print(response.get('insight', 'No insight available'))
        print("─" * 70)
        print(f"📊 Type: {response.get('analysis_type', 'unknown')}")
        print(f"🎯 Confidence: {response.get('confidence', 'unknown').upper()}")
        print()

    def chat_loop(self):
        """Main chat loop"""
        print("\n✅ Chatbot ready! Type 'help' for examples or ask questions.\n")

        while True:
            try:
                user_input = input("🤖 Anda: ").strip()

                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() == 'exit':
                    print("👋 Goodbye! Thank you for using Analytics Chatbot.\n")
                    break
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                elif user_input.lower() == 'history':
                    self.display_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.bot.conversation_history = []
                    print("✓ Chat history cleared\n")
                    continue

                # Process question
                response = self.bot.chat(user_input)
                self.display_response(response)

            except KeyboardInterrupt:
                print("\n\n👋 Session ended by user.\n")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {str(e)}\nTry a different question.\n")
                logger.error(f"Chat error: {str(e)}")

    def run(self):
        """Run the chatbot demo"""
        self.startup()

        if not self.load_data():
            print("❌ Failed to load data. Exiting.\n")
            return False

        self.chat_loop()
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='MNC Analytics Chatbot Demo'
    )
    parser.add_argument(
        '--local',
        action='store_true',
        help='Use local files instead of GitHub'
    )

    args = parser.parse_args()

    demo = ChatbotDemo(use_github=not args.local)
    success = demo.run()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
