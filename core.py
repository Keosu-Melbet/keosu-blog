import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager
from routes import main_bp
from models import Category
from admin_routes import admin_bp  # Nếu bạn có file này

def create_app():
    # Khởi tạo Flask app
    app = Flask(__name__)

    # Cấu hình ứng dụng
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///keosu.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")  # Dùng biến môi trường

    # Xử lý proxy headers (Render, Heroku, v.v.)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Khởi tạo dữ liệu mặc định
    with app.app_context():
        db.create_all()
        _initialize_default_categories(app)

    return app

def _initialize_default_categories(app):
    """Tạo chuyên mục mặc định nếu chưa có"""
    default_categories = ["Ăn uống", "Giải trí", "Học tập", "Mua sắm", "Khác"]
    created = False

    for name in default_categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            created = True

    if created:
        try:
            db.session.commit()
            app.logger.info("Đã tạo chuyên mục mặc định.")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Lỗi khi tạo chuyên mục mặc định: {e}")
