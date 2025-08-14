import os
import logging
from flask import Flask, request, url_for, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from functools import wraps

# Logging
logging.basicConfig(level=logging.DEBUG)

# SQLAlchemy setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///keosu.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Init DB
db.init_app(app)

# Template globals
@app.template_global()
def get_current_year():
    return datetime.now().year

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# -------------------- Admin Middleware --------------------

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Bạn cần đăng nhập để truy cập trang quản trị.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------- Admin Routes --------------------

from models import Admin

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            session['admin_logged_in'] = True
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('manage_articles'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu.', 'error')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@admin_required
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('admin_login'))

# -------------------- App Context --------------------

with app.app_context():
    # Import models and routes
    import models
    import routes

    # Create tables
    db.create_all()

    # Default categories
    from models import Category
    default_categories = [
        {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
        {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
        {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
        {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
        {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
    ]

    for cat_data in default_categories:
        existing = Category.query.filter_by(slug=cat_data['slug']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Lỗi khi tạo danh mục mặc định: {e}")
