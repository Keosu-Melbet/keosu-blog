import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# 🔐 Load biến môi trường từ .env nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 🔌 Extensions
from extensions import db, login_manager

# 📦 Blueprints
from main_routes import main_bp
from admin_routes import admin_bp
from auth import auth_bp  # ✅ Thêm blueprint đăng nhập

# 🔍 SEO utilities
from seo_utils import render_meta_tags, render_structured_data

def create_app():
    """🚀 Tạo và cấu hình Flask app"""
    app = Flask(__name__)

    # ⚙️ Cấu hình ứng dụng
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///keosu.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "UPLOAD_FOLDER": os.getenv("UPLOAD_FOLDER", "static/uploads"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "default-secret-key"),
    })

    # 📁 Đảm bảo thư mục upload tồn tại
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 🛡️ Xử lý proxy headers (Heroku, Render, Nginx)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # 🔌 Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # ✅ Redirect nếu chưa đăng nhập

    # 🔗 Đăng ký blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)  # ✅ Thêm route /auth/login

    # 🌐 Tích hợp hàm SEO vào Jinja
    app.jinja_env.globals['render_meta_tags'] = render_meta_tags
    app.jinja_env.globals['render_structured_data'] = render_structured_data

    # 📋 Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("✅ Flask app đã khởi tạo.")

    return app
