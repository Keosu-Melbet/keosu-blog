from flask import Flask
from .extensions import db
from .routes import main_bp  # Giả sử bạn dùng Blueprint tên main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Đăng ký Blueprint
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

