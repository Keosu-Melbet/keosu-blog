import os
from flask import Flask
from .extensions import db
from .routes import main_bp

def create_app():
    # Xác định đường dẫn tuyệt đối đến thư mục templates
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object('config.Config')

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
