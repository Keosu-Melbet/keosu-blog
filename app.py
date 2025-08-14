import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from routes import bp as main_bp

# Khởi tạo Flask app
app = Flask(__name__)
print("✅ Flask app loaded")

# Cấu hình bảo mật và proxy
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Cấu hình từ file config.py
app.config.from_object(Config)

# Logging
logging.basicConfig(level=logging.DEBUG)

# Khởi tạo SQLAlchemy với DeclarativeBase
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Đăng ký blueprint chính
app.register_blueprint(main_bp)

# Template global: lấy năm hiện tại
@app.template_global()
def get_current_year():
    return datetime.now().year

# Hàm tạo chuyên mục mặc định nếu chưa có
def create_default_categories():
    from models import Category
    default_categories = [
        {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
        {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
        {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
        {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
        {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
    ]
    for cat_data in default_categories:
        existing = Category.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating default categories: {e}")

# Khởi tạo trong app context
with app.app_context():
    import models
    import routes
    import routes_admin

    # Đăng ký blueprint admin
    app.register_blueprint(routes_admin.admin_bp)

    # Tạo bảng nếu chưa có
    db.create_all()

    # Tạo chuyên mục mặc định
    create_default_categories()

# Chạy app nếu là file chính
if __name__ == "__main__":
    app.run(debug=True)
