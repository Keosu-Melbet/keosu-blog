# core.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keosu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.secret_key = 'your-secret-key'  # Thay bằng biến môi trường khi deploy

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from models import Category
        from routes import main_bp
        app.register_blueprint(main_bp)

        db.create_all()

        # Tạo chuyên mục mặc định nếu chưa có
        default_categories = [
            {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
            {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
            {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
            {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
            {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
        ]
        for cat in default_categories:
            if not Category.query.filter_by(slug=cat['slug']).first():
                db.session.add(Category(**cat))
        db.session.commit()

    return app

