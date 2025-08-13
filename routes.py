from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
from models import Article, User, db, Category
from forms import LoginForm, ArticleForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app import app


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Cấu hình upload ảnh
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 🔐 Đăng nhập admin
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = 'Sai tên đăng nhập hoặc mật khẩu.'
    return render_template('admin/login.html', form=form, error=error)

# 🚪 Đăng xuất
@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

# 📋 Trang quản lý bài viết theo chuyên mục
@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    categories = Category.query.filter(Category.slug.in_(['soi-keo', 'meo-cuoc', 'tin-tuc'])).all()
    articles_by_category = {}
    for cat in categories:
        articles = Article.query.filter_by(category_id=cat.id).order_by(Article.created_at.desc()).all()
        articles_by_category[cat.name] = articles
    return render_template('admin/dashboard.html', articles_by_category=articles_by_category)

# ✏️ Tạo bài viết theo chuyên mục
@admin_bp.route('/create/<slug>', methods=['GET', 'POST'])
def create(slug):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    category = Category.query.filter_by(slug=slug).first_or_404()
    form = ArticleForm()
    if form.validate_on_submit():
        image_filename = None
        if form.featured_image.data and allowed_file(form.featured_image.data.filename):
            image_file = form.featured_image.data
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            image_file.save(upload_path)

        article = Article(
            title=form.title.data,
            slug=form.title.data.lower().replace(' ', '-'),
            content=form.content.data,
            excerpt=form.excerpt.data,
            featured_image=image_filename,
            published=form.published.data,
            featured=form.featured.data,
            meta_title=form.meta_title.data,
            meta_description=form.meta_description.data,
            meta_keywords=form.meta_keywords.data,
            category_id=category.id,
            created_at=datetime.utcnow()
        )
        db.session.add(article)
        db.session.commit()
        flash(f'✅ Bài viết đã được tạo trong mục {category.name}!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_article.html', form=form, category=category)

# 🛠 Sửa bài viết
@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    article = Article.query.get_or_404(id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        if form.featured_image.data and allowed_file(form.featured_image.data.filename):
            image_file = form.featured_image.data
            image_filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
            image_file.save(upload_path)
            article.featured_image = image_filename

        form.populate_obj(article)
        article.slug = article.title.lower().replace(' ', '-')
        db.session.commit()
        flash('✅ Bài viết đã được cập nhật!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_article.html', form=form, article=article)

# 🗑 Xóa bài viết
@admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('🗑 Bài viết đã bị xóa!', 'warning')
    return redirect(url_for('admin.dashboard'))
    from flask import render_template
from app import app
from models import Category, Article

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<slug>')
def category_page(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.filter_by(category_id=category.id).all()
    return render_template('category.html', category=category, articles=articles)

