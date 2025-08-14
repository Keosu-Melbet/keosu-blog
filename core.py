from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Cấu hình database (thay đổi nếu cần)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo db với app
    db.init_app(app)

    # Import và đăng ký các blueprint (nếu có)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
