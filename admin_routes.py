from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import Admin, Article, Category
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Đảm bảo có secret key

# -----------------------------
# 🔐 Đăng nhập admin
# -----------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Sai tài khoản hoặc mật khẩu', 'danger')
    return render_template('login.html')

# -----------------------------
# 🚪 Đăng xuất admin
# -----------------------------
@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# -----------------------------
# 📊 Trang tổng quan admin
# -----------------------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_articles = Article.query.count()
    return render_template('dashboard.html', total_articles=total_articles)

# -----------------------------
# 📄 Danh sách bài viết
# -----------------------------
@app.route('/admin/articles')
@login_required
def admin_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles.html', articles=articles)

# -----------------------------
# 📝 Tạo bài viết mới
# -----------------------------
@app.route('/admin/articles/create', methods=['GET', 'POST'])
@login_required
def create_article():
    categories = Category.query.all()
    if request.method == 'POST':
        new_article = Article(
            title=request.form['title'],
            content=request.form['content'],
            category_id=request.form['category'],
            status=request.form['status'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_article)
        db.session.commit()
        flash('Bài viết đã được tạo!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('create_article.html', categories=categories)

# -----------------------------
# ✏️ Chỉnh sửa bài viết
# -----------------------------
@app.route('/admin/articles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.category_id = request.form['category']
        article.status = request.form['status']
        db.session.commit()
        flash('Bài viết đã được cập nhật!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('edit_article.html', article=article, categories=categories)

# -----------------------------
# 🗑️ Xóa bài viết
# -----------------------------
@app.route('/admin/articles/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Bài viết đã bị xóa!', 'warning')
    return redirect(url_for('admin_articles'))

# -----------------------------
# ⚙️ Quản lý nâng cao (nếu có)
# -----------------------------
@app.route('/admin/articles/manage')
@login_required
def manage_articles():
    articles = Article.query.all()
    return render_template('manage_articles.html', articles=articles)
