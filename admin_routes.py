# admin_routes.py
from flask import render_template, request, redirect, url_for, session, flash
from models import Article, Category
from app import app, db  # dùng app và db từ app.py
from datetime import datetime

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Sai thông tin đăng nhập')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('admin_dashboard.html', articles=articles)

@app.route('/admin/create', methods=['GET', 'POST'])
def admin_create_article():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    categories = Category.query.all()
    if request.method == 'POST':
        article = Article(
            title=request.form['title'],
            slug=request.form['slug'],
            content=request.form['content'],
            category_id=request.form['category_id'],
            published=True
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_create_article.html', categories=categories)
