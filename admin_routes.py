from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from models import Admin, Article, Category
from forms import ArticleForm
from core import db
from seo_utils import generate_slug

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Sai tài khoản hoặc mật khẩu', 'danger')
    return render_template('login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_articles = Article.query.count()
    return render_template('dashboard.html', total_articles=total_articles)

@admin_bp.route('/create-article', methods=['GET', 'POST'])
@login_required
def create_article():
    form = ArticleForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            excerpt=form.excerpt.data,
            category_id=form.category_id.data,
            featured_image=form.featured_image.data,
            featured=form.featured.data,
            published=form.published.data,
        )
        db.session.add(article)
        db.session.commit()
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('create_article.html', form=form)

@admin_bp.route('/edit-article/<int:id>', methods=['GET'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    return render_template('admin_edit_article.html', article=article)

@admin_bp.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Vui lòng nhập tên chuyên mục.', 'danger')
            return redirect(url_for('admin.add_category'))

        slug = generate_slug(name)
        if Category.query.filter_by(slug=slug).first():
            flash('Chuyên mục đã tồn tại.', 'warning')
            return redirect(url_for('admin.add_category'))

        new_category = Category(name=name, slug=slug)
        db.session.add(new_category)
        db.session.commit()
        flash('Thêm chuyên mục thành công!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('add_category.html')
