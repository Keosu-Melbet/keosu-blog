from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager
from routes import main_bp
from models import Category
from admin_routes import admin_bp

def create_app():
    app.register_blueprint(admin_bp)
    app = Flask(__name__)

    # Cấu hình ứng dụng
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///keosu.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "static/uploads"
    app.secret_key = "your-secret-key"  # Nên dùng biến môi trường trong production

    # Xử lý proxy headers (Render, Heroku, v.v.)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Đăng ký blueprint và khởi tạo dữ liệu
    with app.app_context():
        app.register_blueprint(main_bp)
        db.create_all()

        # Tạo chuyên mục mặc định nếu chưa có
        default_categories = ["Ăn uống", "Giải trí", "Học tập", "Mua sắm", "Khác"]
        for name in default_categories:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Lỗi khi tạo chuyên mục mặc định: {e}")

    return app
