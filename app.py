from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, Admin
from auth import auth_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route("/")
@login_required
def dashboard():
    return f"Chào mừng {current_user.email} đến trang quản trị!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
