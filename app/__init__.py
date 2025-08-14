from flask import Flask
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # hoặc config riêng của bạn

    db.init_app(app)  # ✅ Đây là dòng quan trọng

    with app.app_context():
        db.create_all()

    return app
