# models.py
from extensions import db
from flask_login import UserMixin
from datetime import datetime
import re

# -----------------------------
# 📁 Category Model
# -----------------------------

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    articles = db.relationship('Article', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SEO fields
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(500))
    
    # Foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def generate_slug(self):
        """Generate URL-friendly slug from title"""
        # Remove Vietnamese diacritics and convert to lowercase
        slug = self.title.lower()
        # Replace spaces with hyphens
        slug = re.sub(r'\s+', '-', slug)
        # Remove special characters
        slug = re.sub(r'[^\w\-]', '', slug)
        return slug
    
    def get_excerpt(self, length=150):
        """Get article excerpt"""
        if self.excerpt:
            return self.excerpt
        # Generate excerpt from content
        text = re.sub(r'<[^>]+>', '', self.content)  # Remove HTML tags
        if len(text) <= length:
            return text
        return text[:length] + '...'

class BettingOdd(db.Model):
    """Model for storing betting odds data"""
    id = db.Column(db.Integer, primary_key=True)
    match_name = db.Column(db.String(200), nullable=False)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    league = db.Column(db.String(100))
    
    # Odds
    home_win = db.Column(db.Float)
    draw = db.Column(db.Float)
    away_win = db.Column(db.Float)
    over_2_5 = db.Column(db.Float)
    under_2_5 = db.Column(db.Float)
    
    # Asian Handicap
    handicap = db.Column(db.String(10))
    handicap_home = db.Column(db.Float)
    handicap_away = db.Column(db.Float)
    
    # Recommendation
    recommendation = db.Column(db.String(200))
    confidence = db.Column(db.Integer)  # 1-5 scale
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BettingOdd {self.home_team} vs {self.away_team}>'

class Match(db.Model):
    """Model for match schedule"""
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    league = db.Column(db.String(100))
    venue = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, live, finished
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Match {self.home_team} vs {self.away_team}>'


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

