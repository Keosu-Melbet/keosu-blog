from flask_sqlalchemy import SQLAlchemy
from .extensions import db
from datetime import datetime
from sqlalchemy import event
import re
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# -------------------- Admin --------------------

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'

# -------------------- Category --------------------

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    articles = db.relationship('Article', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

# -------------------- Article --------------------

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(500))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'

    def generate_slug(self):
        slug = self.title.lower()
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'[^\w\-]', '', slug)
        return slug

    def get_excerpt(self, length=150):
        if self.excerpt:
            return self.excerpt
        text = re.sub(r'<[^>]+>', '', self.content)
        return text[:length] + '...' if len(text) > length else text

    def get_image_url(self):
        if self.featured_image:
            return f'/static/uploads/{self.featured_image}'
        return None

@event.listens_for(Article, 'before_insert')
def generate_article_slug(mapper, connection, target):
    if not target.slug:
        target.slug = target.generate_slug()

# -------------------- Betting Odds --------------------

class BettingOdd(db.Model):
    __tablename__ = 'betting_odds'

    id = db.Column(db.Integer, primary_key=True)
    match_name = db.Column(db.String(200), nullable=False)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    league = db.Column(db.String(100))

    home_win = db.Column(db.Float)
    draw = db.Column(db.Float)
    away_win = db.Column(db.Float)
    over_2_5 = db.Column(db.Float)
    under_2_5 = db.Column(db.Float)

    handicap = db.Column(db.String(10))
    handicap_home = db.Column(db.Float)
    handicap_away = db.Column(db.Float)

    recommendation = db.Column(db.String(200))
    confidence = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<BettingOdd {self.home_team} vs {self.away_team}>'

# -------------------- Match --------------------

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    match_date = db.Column(db.DateTime, nullable=False)
    league = db.Column(db.String(100))
    venue = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Match {self.home_team} vs {self.away_team}>'
