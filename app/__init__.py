from flask import Flask
from .extensions import db
from .routes import *  # Import routes sau khi app được tạo

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

with app.app_context():
    db.create_all()
