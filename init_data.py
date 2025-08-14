#!/usr/bin/env python3
"""
Initialize sample data for Kèo Sư website
This script populates the database with realistic Vietnamese football content
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Article, BettingOdd, Match

def create_sample_articles():
    """Create sample articles for different categories"""
    keo_thom = Category.query.filter_by(slug='keo-thom').first()
    soi_keo = Category.query.filter_by(slug='soi-keo').first()
    meo_cuoc = Category.query.filter_by(slug='meo-cuoc').first()
    tin_tuc = Category.query.filter_by(slug='tin-tuc').first()

    sample_articles = [
        {
            'title': 'Kèo thơm hôm nay: Manchester United vs Arsenal - Cơ hội vàng cho Quỷ đỏ',
            'slug': 'keo-thom-man-united-vs-arsenal-co-hoi-vang',
            'content': '<h2>Phân tích trận đấu...</h2>',
            'excerpt': 'Phân tích chi tiết trận Manchester United vs Arsenal...',
            'category_id': keo_thom.id if keo_thom else 1,
            'featured': True,
            'meta_title': 'Kèo thơm Man United vs Arsenal...',
            'meta_description': 'Phân tích kèo thơm trận Manchester United vs Arsenal...',
            'meta_keywords': 'kèo thơm, manchester united, arsenal...',
            'featured_image': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800'
        },
        # Các bài viết khác tương tự...
    ]

    for article_data in sample_articles:
        existing = Article.query.filter_by(slug=article_data['slug']).first()
        if not existing:
            if 'views' not in article_data:
                article_data['views'] = random.randint(50, 300)
            article = Article(**article_data)
            db.session.add(article)

    try:
        db.session.commit()
        print(f"✅ Created {len(sample_articles)} sample articles")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating articles: {e}")

def create_sample_betting_odds():
    """Create sample betting odds for today and tomorrow"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    matches_data = [
        {
            'home_team': 'Manchester United',
            'away_team': 'Arsenal',
            'match_date': today.replace(hour=21, minute=0),
            'league': 'Premier League',
            'home_win': 2.20,
            'draw': 3.40,
            'away_win': 3.10,
            'over_2_5': 1.85,
            'under_2_5': 1.95,
            'handicap': '-0.5',
            'handicap_home': 1.90,
            'handicap_away': 1.90,
            'recommendation': 'Chủ nhà thắng',
            'confidence': 4
        },
        # Các trận khác tương tự...
    ]

    for match_data in matches_data:
        match_data['match_name'] = f"{match_data['home_team']} vs {match_data['away_team']}"
        existing = BettingOdd.query.filter_by(
            home_team=match_data['home_team'],
            away_team=match_data['away_team'],
            match_date=match_data['match_date']
        ).first()
        if not existing:
            odd = BettingOdd(**match_data)
            db.session.add(odd)

    try:
        db.session.commit()
        print(f"✅ Created {len(matches_data)} betting odds")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating betting odds: {e}")

def create_sample_matches():
    """Create sample match schedule"""
    today = datetime.now()
    matches_schedule = []

    for i in range(7):
        match_date = today + timedelta(days=i)
        daily_matches = [
            {
                'home_team': 'Manchester City',
                'away_team': 'Tottenham',
                'match_date': match_date.replace(hour=20, minute=0),
                'league': 'Premier League',
                'venue': 'Etihad Stadium',
                'status': 'scheduled'
            },
            {
                'home_team': 'PSG',
                'away_team': 'Lyon',
                'match_date': match_date.replace(hour=22, minute=0),
                'league': 'Ligue 1',
                'venue': 'Parc des Princes',
                'status': 'scheduled'
            }
        ]
        matches_schedule.extend(daily_matches)

    finished_matches = [
        {
            'home_team': 'Arsenal',
            'away_team': 'Chelsea',
            'match_date': today - timedelta(days=1),
            'league': 'Premier League',
            'venue': 'Emirates Stadium',
            'status': 'finished',
            'home_score': 2,
            'away_score': 1
        },
        {
            'home_team': 'Real Madrid',
            'away_team': 'Atletico Madrid',
            'match_date': today - timedelta(days=2),
            'league': 'La Liga',
            'venue': 'Santiago Bernabeu',
            'status': 'finished',
            'home_score': 3,
            'away_score': 1
        }
    ]
    matches_schedule.extend(finished_matches)

    for match_data in matches_schedule:
        existing = Match.query.filter_by(
            home_team=match_data['home_team'],
            away_team=match_data['away_team'],
            match_date=match_data['match_date']
        ).first()
        if not existing:
            match = Match(**match_data)
            db.session.add(match)

    try:
        db.session.commit()
        print(f"✅ Created {len(matches_schedule)} match schedules")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating matches: {e}")

def main():
    """Main function to initialize all sample data"""
    print("🚀 Initializing sample data for Kèo Sư website...")
    with app.app_context():
        create_sample_articles()
        create_sample_betting_odds()
        create_sample_matches()
        print("✅ Sample data initialization completed!")
        print("\n📊 Database Summary:")
        print(f" • Categories: {Category.query.count()}")
        print(f" • Articles: {Article.query.count()}")
        print(f" • Betting Odds: {BettingOdd.query.count()}")
        print(f" • Matches: {Match.query.count()}")
        print("\n🌐 You can now start the website with: python main.py")

if __name__ == '__main__':
    main()
