#!/usr/bin/env python3
"""
Khởi tạo dữ liệu mẫu cho website Kèo Sư
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Thêm thư mục hiện tại vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Article, BettingOdd, Match

def create_sample_articles():
    """Tạo bài viết mẫu"""
    categories = {
        'keo-thom': Category.query.filter_by(slug='keo-thom').first(),
        'soi-keo': Category.query.filter_by(slug='soi-keo').first(),
        'meo-cuoc': Category.query.filter_by(slug='meo-cuoc').first(),
        'tin-tuc': Category.query.filter_by(slug='tin-tuc').first()
    }

    sample_articles = [
        {
            'title': 'Kèo thơm hôm nay: Manchester United vs Arsenal - Cơ hội vàng cho Quỷ đỏ',
            'slug': 'keo-thom-man-united-vs-arsenal-co-hoi-vang',
            'excerpt': 'Phân tích chi tiết trận Manchester United vs Arsenal với những kèo thơm hấp dẫn cho người chơi.',
            'category_id': categories['keo-thom'].id if categories['keo-thom'] else 1,
            'featured': True,
            'meta_title': 'Kèo thơm Man United vs Arsenal - Phân tích chuyên sâu | Kèo Sư',
            'meta_description': 'Phân tích kèo thơm trận Manchester United vs Arsenal với dự đoán tỷ số chính xác và tỷ lệ kèo hấp dẫn.',
            'meta_keywords': 'kèo thơm, manchester united, arsenal, premier league, dự đoán tỷ số',
            'featured_image': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800',
            'content': '<h2>Phân tích trận đấu...</h2>',
        },
        # Thêm các bài viết khác tương tự...
    ]

    for data in sample_articles:
        if not Article.query.filter_by(slug=data['slug']).first():
            data['views'] = random.randint(100, 500)
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()
            article = Article(**data)
            db.session.add(article)

    try:
        db.session.commit()
        print(f"✅ Created {len(sample_articles)} sample articles")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating articles: {e}")

def create_sample_betting_odds():
    """Tạo tỷ lệ cược mẫu"""
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
        # Thêm các trận khác...
    ]

    for data in matches_data:
        data['match_name'] = f"{data['home_team']} vs {data['away_team']}"
        if not BettingOdd.query.filter_by(
            home_team=data['home_team'],
            away_team=data['away_team'],
            match_date=data['match_date']
        ).first():
            data['created_at'] = datetime.utcnow()
            odd = BettingOdd(**data)
            db.session.add(odd)

    try:
        db.session.commit()
        print(f"✅ Created {len(matches_data)} betting odds")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating betting odds: {e}")

def create_sample_matches():
    """Tạo lịch thi đấu mẫu"""
    today = datetime.now()
    schedule = []

    for i in range(7):
        date = today + timedelta(days=i)
        schedule.extend([
            {
                'home_team': 'Manchester City',
                'away_team': 'Tottenham',
                'match_date': date.replace(hour=20),
                'league': 'Premier League',
                'venue': 'Etihad Stadium',
                'status': 'scheduled'
            },
            {
                'home_team': 'PSG',
                'away_team': 'Lyon',
                'match_date': date.replace(hour=22),
                'league': 'Ligue 1',
                'venue': 'Parc des Princes',
                'status': 'scheduled'
            }
        ])

    schedule.extend([
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
            'venue': 'Bernabeu',
            'status': 'finished',
            'home_score': 3,
            'away_score': 1
        }
    ])

    for data in schedule:
        if not Match.query.filter_by(
            home_team=data['home_team'],
            away_team=data['away_team'],
            match_date=data['match_date']
        ).first():
            data['created_at'] = datetime.utcnow()
            match = Match(**data)
            db.session.add(match)

    try:
        db.session.commit()
        print(f"✅ Created {len(schedule)} match schedules")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating matches: {e}")

def initialize_sample_data():
    """Khởi tạo toàn bộ dữ liệu mẫu"""
    create_sample_articles()
    create_sample_betting_odds()
    create_sample_matches()

def main():
    print("🚀 Đang khởi tạo dữ liệu mẫu cho Kèo Sư...")
    with app.app_context():
        initialize_sample_data()
        print("\n📊 Tổng kết dữ liệu:")
        print(f"   • Categories: {Category.query.count()}")
        print(f"   • Articles: {Article.query.count()}")
        print(f"   • Betting Odds: {BettingOdd.query.count()}")
        print(f"   • Matches: {Match.query.count()}")
        print("\n🌐 Khởi chạy website bằng: python main.py")

if __name__ == '__main__':
    main()
