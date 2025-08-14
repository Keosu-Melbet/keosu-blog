import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from .extensions import db
from .models import Category

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Config
    app.config.from_object('config.Config')

    # Init extensions
    db.init_app(app)

    # Template globals
    @app.template_global()
    def get_current_year():
        return datetime.now().year

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    # Register routes
    from .routes import register_routes
    register_routes(app)

    # Create tables + default categories
    with app.app_context():
        db.create_all()
        default_categories = [
            {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
            {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
            {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
            {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
            {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
        ]
        for cat_data in default_categories:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                db.session.add(Category(**cat_data))
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Lỗi khi tạo danh mục mặc định: {e}")

    return app
