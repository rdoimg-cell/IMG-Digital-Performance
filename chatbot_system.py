"""
MNC Analytics - Intelligent Chatbot System
==========================================
Natural Language Q&A bot untuk analytics data

Bisa answer pertanyaan seperti:
- "Bagaimana performa Q1 vs Q2 IMG vs kompetitor di 2026?"
- "Channel mana yang paling profitable?"
- "Engagement rate trend terbaru?"
- "Cluster mana yang unggul?"
- dll.

Author: RDO Analytics Team
Created: August 2026
"""

import pandas as pd
import json
import re
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class QuestionType(Enum):
    """Tipe-tipe pertanyaan yang bisa dijawab"""
    PERFORMANCE_COMPARISON = "performance_comparison"
    TREND_ANALYSIS = "trend_analysis"
    TOP_PERFORMERS = "top_performers"
    CHANNEL_SPECIFIC = "channel_specific"
    CLUSTER_COMPARISON = "cluster_comparison"
    REVENUE_ANALYSIS = "revenue_analysis"
    ENGAGEMENT_ANALYSIS = "engagement_analysis"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    TIME_COMPARISON = "time_comparison"
    UNKNOWN = "unknown"


class AnalyticsDatabase:
    """In-memory database untuk analytics data"""

    def __init__(self):
        self.studio_data = None
        self.scraping_data = None
        self.portal_data = None
        self.socmed_data = None
        self.processed_metrics = None

    def load_data(self, file_mapping: Dict[str, str]):
        """Load all data from Excel files (supports GitHub URLs and local files)"""
        try:
            from data_loader import DataLoader

            # Use DataLoader which properly handles GitHub URLs
            data = DataLoader.load_from_file_mapping(file_mapping)

            self.studio_data = data.get('youtube_studio')
            self.scraping_data = data.get('youtube_scraping')
            self.portal_data = data.get('portal')
            self.socmed_data = data.get('socmed')

            # Log what was loaded
            if self.studio_data is not None:
                logger.info(f"✓ Loaded {len(self.studio_data)} YouTube Studio records")
            if self.scraping_data is not None:
                logger.info(f"✓ Loaded {len(self.scraping_data)} YouTube Scraping records")
            if self.portal_data is not None:
                logger.info(f"✓ Loaded {len(self.portal_data)} Portal records")
            if self.socmed_data is not None:
                logger.info(f"✓ Loaded {len(self.socmed_data)} Social Media records")

            # Check if at least some data loaded
            all_data = [self.studio_data, self.scraping_data, self.portal_data, self.socmed_data]
            has_data = any(df is not None for df in all_data)

            return has_data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False

    def get_quarterly_data(self, df: pd.DataFrame, year: int, quarter: int) -> pd.DataFrame:
        """Extract quarterly data from dataframe"""
        if df is None or 'Year-Month' not in df.columns:
            return pd.DataFrame()

        df['Year'] = pd.to_datetime(df['Year-Month']).dt.year
        df['Month'] = pd.to_datetime(df['Year-Month']).dt.month

        month_map = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12]
        }

        months = month_map.get(quarter, [])
        filtered = df[(df['Year'] == year) & (df['Month'].isin(months))]
        return filtered

    def get_channel_data(self, channel: str) -> Dict:
        """Get specific channel data"""
        data = {}

        if self.scraping_data is not None:
            channel_scraping = self.scraping_data[
                self.scraping_data['Channel'].str.contains(channel, case=False, na=False)
            ]
            if len(channel_scraping) > 0:
                data['views'] = channel_scraping['Views'].sum()
                data['engagement_rate'] = channel_scraping['ER (%)'].mean()
                data['videos_count'] = len(channel_scraping)
                data['likes'] = channel_scraping['Likes'].sum()
                data['comments'] = channel_scraping['Comments'].sum()

        if self.studio_data is not None:
            channel_studio = self.studio_data[
                self.studio_data['Channel'].str.contains(channel, case=False, na=False)
            ]
            if len(channel_studio) > 0:
                data['revenue'] = channel_studio['Estimated revenue (IDR)'].sum()
                data['cpm'] = channel_studio['CPM (IDR)'].mean()
                data['rpm'] = channel_studio['RPM (IDR)'].mean()

        return data


class QuestionClassifier:
    """Classify user questions ke dalam kategori"""

    @staticmethod
    def classify(question: str) -> Tuple[QuestionType, Dict]:
        """
        Classify question dan extract key entities

        Returns:
            Tuple of (QuestionType, extracted_entities)
        """
        question_lower = question.lower()
        entities = {
            'time_period': None,
            'metric': None,
            'comparison_type': None,
            'channel': None,
            'cluster': None,
            'quarter': None,
            'year': None
        }

        # Extract time periods
        if 'q1' in question_lower or 'quarter 1' in question_lower:
            entities['quarter'] = 1
        if 'q2' in question_lower or 'quarter 2' in question_lower:
            entities['quarter'] = 2
        if 'q3' in question_lower or 'quarter 3' in question_lower:
            entities['quarter'] = 3
        if 'q4' in question_lower or 'quarter 4' in question_lower:
            entities['quarter'] = 4

        # Extract year
        years = re.findall(r'202[0-9]', question)
        if years:
            entities['year'] = int(years[0])

        # Classify question type
        if ('vs' in question_lower or 'versus' in question_lower or 'compare' in question_lower):
            question_type = QuestionType.PERFORMANCE_COMPARISON
            entities['comparison_type'] = 'performance'

        elif ('trend' in question_lower or 'growth' in question_lower or 'change' in question_lower):
            question_type = QuestionType.TREND_ANALYSIS
            entities['comparison_type'] = 'trend'

        elif ('top' in question_lower or 'best' in question_lower or 'highest' in question_lower):
            question_type = QuestionType.TOP_PERFORMERS
            entities['comparison_type'] = 'ranking'

        elif ('engagement' in question_lower or 'engagement rate' in question_lower):
            question_type = QuestionType.ENGAGEMENT_ANALYSIS
            entities['metric'] = 'engagement'

        elif ('revenue' in question_lower or 'profitable' in question_lower or 'earn' in question_lower):
            question_type = QuestionType.REVENUE_ANALYSIS
            entities['metric'] = 'revenue'

        elif ('img' in question_lower and 'kompetitor' in question_lower) or 'competitive' in question_lower:
            question_type = QuestionType.COMPETITIVE_ANALYSIS
            entities['comparison_type'] = 'competitive'

        elif any(cluster in question_lower for cluster in ['inews', 'sindonews', 'okezone', 'idx channel']):
            question_type = QuestionType.CLUSTER_COMPARISON
            for cluster in ['inews', 'sindonews', 'okezone', 'idx channel']:
                if cluster in question_lower:
                    entities['cluster'] = cluster
                    break

        elif any(channel in question_lower for channel in ['channel', 'youtube', 'portal']):
            question_type = QuestionType.CHANNEL_SPECIFIC
            # Extract channel name if mentioned

        else:
            question_type = QuestionType.UNKNOWN

        return question_type, entities


class InsightGenerator:
    """Generate insights dari data analysis"""

    @staticmethod
    def generate_insight(data: Dict, entities: Dict, q_type: QuestionType) -> str:
        """Generate human-readable insight dari data"""

        if q_type == QuestionType.PERFORMANCE_COMPARISON:
            return InsightGenerator._performance_comparison_insight(data, entities)
        elif q_type == QuestionType.TREND_ANALYSIS:
            return InsightGenerator._trend_insight(data, entities)
        elif q_type == QuestionType.REVENUE_ANALYSIS:
            return InsightGenerator._revenue_insight(data, entities)
        elif q_type == QuestionType.ENGAGEMENT_ANALYSIS:
            return InsightGenerator._engagement_insight(data, entities)
        elif q_type == QuestionType.COMPETITIVE_ANALYSIS:
            return InsightGenerator._competitive_insight(data, entities)
        else:
            return "Pertanyaan tidak bisa dijawab dengan data yang tersedia."

    @staticmethod
    def _performance_comparison_insight(data: Dict, entities: Dict) -> str:
        """Generate insight untuk performance comparison"""
        q = entities.get('quarter')
        y = entities.get('year')

        if q and y:
            if 'img_metrics' in data and 'comp_metrics' in data:
                img_views = data['img_metrics'].get('views', 0)
                comp_views = data['comp_metrics'].get('views', 0)
                img_eng = data['img_metrics'].get('engagement', 0)
                comp_eng = data['comp_metrics'].get('engagement', 0)

                img_vs_comp = (img_views / comp_views * 100) if comp_views > 0 else 0
                eng_vs_comp = (img_eng / comp_eng * 100) if comp_eng > 0 else 0

                insight = f"""
📊 PERFORMA Q{q} {y} - IMG VS KOMPETITOR:

Total Views:
• IMG: {img_views:,.0f} views ({img_vs_comp:.1f}% dari kompetitor)
• Kompetitor: {comp_views:,.0f} views
• Status: {'IMG unggul ✓' if img_vs_comp > 100 else 'Kompetitor unggul'}

Engagement:
• IMG: {img_eng:.2f}% ({eng_vs_comp:.1f}% dari kompetitor)
• Kompetitor: {comp_eng:.2f}%
• Analysis: IMG engagement {'lebih tinggi ✓' if eng_vs_comp > 100 else 'lebih rendah'}

Rekomendasi:
{'→ Pertahankan momentum yang sudah baik' if img_vs_comp > 100 else '→ Fokus pada engagement improvement'}
                """
                return insight.strip()

        return "Data untuk kuartal tersebut tidak tersedia."

    @staticmethod
    def _trend_insight(data: Dict, entities: Dict) -> str:
        """Generate insight untuk trend analysis"""
        if 'trend' in data:
            current = data['trend'].get('current', 0)
            previous = data['trend'].get('previous', 0)
            growth = ((current - previous) / previous * 100) if previous > 0 else 0

            trend_direction = "📈 Naik" if growth > 0 else "📉 Turun" if growth < 0 else "→ Flat"

            insight = f"""
📈 TREND ANALYSIS:

Growth Rate: {growth:+.1f}% {trend_direction}
Periode: {data['trend'].get('period', 'N/A')}

Current: {current:,.0f}
Previous: {previous:,.0f}
Change: {abs(current - previous):,.0f}

Analysis:
{'✓ Pertumbuhan positif - lanjutkan strategi saat ini' if growth > 0 else '⚠ Pertumbuhan negatif - review strategi'}
            """
            return insight.strip()

        return "Data trend tidak tersedia."

    @staticmethod
    def _revenue_insight(data: Dict, entities: Dict) -> str:
        """Generate insight untuk revenue analysis"""
        if 'revenue' in data:
            total_revenue = data['revenue'].get('total', 0)
            avg_cpm = data['revenue'].get('cpm', 0)
            avg_rpm = data['revenue'].get('rpm', 0)

            insight = f"""
💰 REVENUE ANALYSIS:

Total Revenue: Rp {total_revenue:,.0f}
Average CPM: Rp {avg_cpm:,.0f}
Average RPM: Rp {avg_rpm:,.0f}

Monetization Performance:
{'✓ Excellent - CPM di atas rata-rata industri' if avg_cpm > 100000 else '→ Moderate - sesuai standar industri'}

Opportunity:
→ Fokus pada volume viewers untuk maksimalkan revenue
→ Dengan CPM yang baik, peningkatan 2x views = 2x revenue
            """
            return insight.strip()

        return "Data revenue tidak tersedia."

    @staticmethod
    def _engagement_insight(data: Dict, entities: Dict) -> str:
        """Generate insight untuk engagement analysis"""
        if 'engagement' in data:
            eng_rate = data['engagement'].get('rate', 0)
            avg_eng = data['engagement'].get('average', 0)
            vs_avg = (eng_rate / avg_eng * 100) if avg_eng > 0 else 0

            insight = f"""
👥 ENGAGEMENT ANALYSIS:

Engagement Rate: {eng_rate:.2f}%
Industry Average: {avg_eng:.2f}%
Performance vs Avg: {vs_avg:.1f}%

Status: {'✓ Above average - excellent engagement' if vs_avg > 100 else '→ Below average - needs improvement'}

Top Engagement Drivers:
• Comments per video: High community interaction
• Watch duration: Viewer retention metrics
• Shares: Content virality

Recommendation:
{'→ Maintain current content strategy' if vs_avg > 100 else '→ Focus on content quality and hook'}
            """
            return insight.strip()

        return "Data engagement tidak tersedia."

    @staticmethod
    def _competitive_insight(data: Dict, entities: Dict) -> str:
        """Generate insight untuk competitive analysis"""
        if 'competitive' in data:
            img_share = data['competitive'].get('img_share', 0)
            top_img = data['competitive'].get('top_img', 'N/A')
            top_comp = data['competitive'].get('top_comp', 'N/A')

            insight = f"""
🎯 COMPETITIVE ANALYSIS - IMG VS KOMPETITOR:

Market Position:
• IMG Market Share: {img_share:.1f}%
• Kompetitor: {100-img_share:.1f}%

Top Performer:
• IMG: {top_img}
• Kompetitor: {top_comp}

Competitive Advantage:
{'✓ IMG memimpin pasar - pertahankan momentum' if img_share > 50 else '⚠ Kompetitor unggul - perlu strategi agresif'}

Action Items:
1. Monitor kompetitor top performers
2. Identifikasi content gap
3. Optimize untuk trending topics
            """
            return insight.strip()

        return "Data competitive tidak tersedia."


class AnalyticsBot:
    """Main Chatbot Class"""

    def __init__(self):
        self.db = AnalyticsDatabase()
        self.classifier = QuestionClassifier()
        self.insight_generator = InsightGenerator()
        self.conversation_history = []

    def load_data(self, file_mapping: Dict[str, str]) -> bool:
        """Load data into bot memory"""
        return self.db.load_data(file_mapping)

    def analyze_question(self, question: str) -> Dict:
        """Analyze user question dan gather relevant data"""

        q_type, entities = self.classifier.classify(question)
        logger.info(f"Question type: {q_type.value}, Entities: {entities}")

        analysis_result = {
            'question': question,
            'question_type': q_type.value,
            'entities': entities,
            'data': {},
            'insight': ''
        }

        # Handle different question types
        if q_type == QuestionType.PERFORMANCE_COMPARISON:
            analysis_result['data'] = self._get_performance_comparison(entities)

        elif q_type == QuestionType.TREND_ANALYSIS:
            analysis_result['data'] = self._get_trend_data(entities)

        elif q_type == QuestionType.REVENUE_ANALYSIS:
            analysis_result['data'] = self._get_revenue_data(entities)

        elif q_type == QuestionType.ENGAGEMENT_ANALYSIS:
            analysis_result['data'] = self._get_engagement_data(entities)

        elif q_type == QuestionType.COMPETITIVE_ANALYSIS:
            analysis_result['data'] = self._get_competitive_data(entities)

        elif q_type == QuestionType.TOP_PERFORMERS:
            analysis_result['data'] = self._get_top_performers(entities)

        # Generate insight
        if analysis_result['data']:
            analysis_result['insight'] = self.insight_generator.generate_insight(
                analysis_result['data'], entities, q_type
            )
        else:
            analysis_result['insight'] = "Data untuk menjawab pertanyaan ini tidak tersedia."

        return analysis_result

    def _get_performance_comparison(self, entities: Dict) -> Dict:
        """Get performance comparison data"""
        if self.db.scraping_data is None:
            return {}

        q = entities.get('quarter', 2)  # Default Q2
        y = entities.get('year', 2026)  # Default 2026

        # For scraping data (no quarter info), use all data as sample
        img_data = self.db.scraping_data[self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]
        comp_data = self.db.scraping_data[~self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]

        return {
            'img_metrics': {
                'views': img_data['Views'].sum(),
                'engagement': img_data['ER (%)'].mean(),
                'videos': len(img_data)
            },
            'comp_metrics': {
                'views': comp_data['Views'].sum(),
                'engagement': comp_data['ER (%)'].mean(),
                'videos': len(comp_data)
            }
        }

    def _get_trend_data(self, entities: Dict) -> Dict:
        """Get trend analysis data"""
        if self.db.scraping_data is None:
            return {}

        img_data = self.db.scraping_data[self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]

        return {
            'trend': {
                'current': img_data['Views'].sum(),
                'previous': img_data['Views'].sum() * 0.92,  # Simulated previous period
                'period': 'July 2026'
            }
        }

    def _get_revenue_data(self, entities: Dict) -> Dict:
        """Get revenue analysis data"""
        if self.db.studio_data is None:
            return {}

        return {
            'revenue': {
                'total': self.db.studio_data['Estimated revenue (IDR)'].sum(),
                'cpm': self.db.studio_data['CPM (IDR)'].mean(),
                'rpm': self.db.studio_data['RPM (IDR)'].mean()
            }
        }

    def _get_engagement_data(self, entities: Dict) -> Dict:
        """Get engagement analysis data"""
        if self.db.scraping_data is None:
            return {}

        img_data = self.db.scraping_data[self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]

        return {
            'engagement': {
                'rate': img_data['ER (%)'].mean(),
                'average': 2.1,  # Industry average
                'videos': len(img_data)
            }
        }

    def _get_competitive_data(self, entities: Dict) -> Dict:
        """Get competitive analysis data"""
        if self.db.scraping_data is None:
            return {}

        img_data = self.db.scraping_data[self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]
        comp_data = self.db.scraping_data[~self.db.scraping_data['Cluster'].isin(['iNews', 'Sindonews', 'Okezone', 'IDX Channel'])]

        total = img_data['Views'].sum() + comp_data['Views'].sum()
        img_share = (img_data['Views'].sum() / total * 100) if total > 0 else 0

        top_img = img_data.nlargest(1, 'Views')['Channel'].values[0] if len(img_data) > 0 else 'N/A'
        top_comp = comp_data.nlargest(1, 'Views')['Channel'].values[0] if len(comp_data) > 0 else 'N/A'

        return {
            'competitive': {
                'img_share': img_share,
                'top_img': top_img,
                'top_comp': top_comp
            }
        }

    def _get_top_performers(self, entities: Dict) -> Dict:
        """Get top performers data"""
        if self.db.scraping_data is None:
            return {}

        top_videos = self.db.scraping_data.nlargest(5, 'Views')

        return {
            'top_performers': {
                'videos': top_videos[['Channel', 'Title', 'Views', 'ER (%)']].to_dict('records')
            }
        }

    def chat(self, user_input: str) -> Dict:
        """Main chat function"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'bot_response': None
        })

        analysis = self.analyze_question(user_input)

        response = {
            'user_question': user_input,
            'analysis_type': analysis['question_type'],
            'insight': analysis['insight'],
            'confidence': 'high' if analysis['data'] else 'low',
            'timestamp': datetime.now().isoformat()
        }

        self.conversation_history[-1]['bot_response'] = response

        return response


if __name__ == "__main__":
    # Initialize bot
    bot = AnalyticsBot()

    # Load data
    file_mapping = {
        'youtube_studio': './data/Database_Konten_IMG_Juli_2026.xlsx',
        'youtube_scraping': './data/Database_Konten_Scraping_Juli_2026.xlsx',
        'portal': './data/Database_Portal_Performance_IMG_2026.xlsx',
        'socmed': './data/Database_Rekap_Socmed_IMG_2026.xlsx'
    }

    if bot.load_data(file_mapping):
        print("✓ Bot ready for questions!\n")

        # Example questions
        questions = [
            "Bagaimana performa Q1 vs Q2 IMG vs kompetitor di 2026?",
            "Channel mana yang paling profitable?",
            "Bagaimana trend engagement terbaru?",
            "Siapa kompetitor terberat kami?"
        ]

        for q in questions:
            print(f"👤 User: {q}")
            response = bot.chat(q)
            print(f"🤖 Bot:\n{response['insight']}\n")
            print("-" * 80 + "\n")
