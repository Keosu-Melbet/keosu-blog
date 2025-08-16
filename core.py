import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Load biến môi trường từ .env nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Extensions
from extensions import db, login_manager

# Blueprints
from main_routes import main_bp
from admin_routes import admin_bp

# Models
from models import Category

def create_app():
    app = Flask(__name__)

    # 🔧 Cấu hình ứng dụng
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///keosu.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "UPLOAD_FOLDER": os.getenv("UPLOAD_FOLDER", "static/uploads"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "default-secret-key"),
    })

    # 📁 Đảm bảo thư mục upload tồn tại
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 🛡️ Xử lý proxy headers (nếu deploy qua Nginx, Heroku, v.v.)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # 🔌 Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)

    # 🔗 Đăng ký các blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # 🧱 Khởi tạo dữ liệu mặc định
    with app.app_context():
        db.create_all()
        _initialize_default_categories(app)

    # 📋 Logging cơ bản
    logging.basicConfig(level=logging.INFO)
    app.logger.info("✅ Ứng dụng Flask đã khởi tạo thành công.")

    return app

def _initialize_default_categories(app):
    default_categories = ["Ăn uống", "Giải trí", "Học tập", "Mua sắm", "Khác"]
    created = False

    for name in default_categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            created = True

    if created:
        try:
            db.session.commit()
            app.logger.info("✅ Đã tạo chuyên mục mặc định.")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ Lỗi khi tạo chuyên mục mặc định: {e}")
