import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

from core import create_app, db, login_manager
from routes import app_routes
from supabase_client import supabase

# Logging setup
logging.basicConfig(level=logging.DEBUG)

# SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# Create Flask app
app = create_app()
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///keosu.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Register routes
app.register_blueprint(app_routes)

# Template global: current year
@app.template_global()
def get_current_year():
    return datetime.now().year

# App context setup
with app.app_context():
    # Import models and extra routes
    import models
    import admin_upload

    # Create tables
    db.create_all()

    # Create default categories
    from models import Category
    default_categories = [
        {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
        {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
        {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
        {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
        {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
    ]

    with db.session.no_autoflush:
        for cat_data in default_categories:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                db.session.add(Category(**cat_data))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating default categories: {e}")

# Run app
if __name__ == "__main__":
    app.run(debug=True)
