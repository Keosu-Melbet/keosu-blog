from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, make_response
)
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)
from models import Admin, Article, Category, BettingOdd, Match
from forms import ArticleForm, ContactForm, SearchForm
from werkzeug.security import check_password_hash
from seo_utils import generate_meta_tags
from sqlalchemy import or_, desc
from core import db
from datetime import datetime, timedelta
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return 'Hello from main_bp!'

app = Flask(__name__)
@app.route('/')
def index():
    featured = Article.query.filter_by(published=True, featured=True).limit(3).all()
    recent = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(6).all()

    meta_tags = generate_meta_tags(
        title="Kèo Sư - Website Kèo Bóng Đá Chuyên Nghiệp",
        description="Kèo Sư cung cấp tỷ lệ kèo, soi kèo, mẹo cược bóng đá chính xác.",
        keywords="kèo bóng đá, tỷ lệ kèo, soi kèo"
    )
    return render_template('index.html', featured_articles=featured, recent_articles=recent, meta_tags=meta_tags)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Kiểm tra thông tin đăng nhập từ Supabase
        data = supabase.table("admins").select("*").eq("email", email).eq("password", password).execute()
        if data.data:
            session['user'] = email
            return redirect('/dashboard')
        else:
            return "Sai thông tin đăng nhập", 401

    return render_template('login.html')


# Test route để kiểm tra Supabase
@app.route("/test")
def test():
    data = supabase.table("admins").select("*").execute()
    return str(data.data)


@app.route('/keo-thom')
def keo_thom():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    odds = BettingOdd.query.join(Match).filter(
        Match.match_date >= today,
        Match.match_date < tomorrow
    ).all()

    meta_tags = generate_meta_tags(
        title="Kèo Thơm Hôm Nay | Kèo Sư",
        description="Cập nhật kèo thơm hôm nay, tỷ lệ kèo bóng đá chính xác.",
        keywords="kèo thơm hôm nay, tỷ lệ kèo"
    )
    return render_template('keo-thom.html', odds=odds, meta_tags=meta_tags)


@app.route('/lich-thi-dau')
def lich_thi_dau():
    date_str = request.args.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()
    except ValueError:
        selected_date = datetime.now().date()

    next_date = selected_date + timedelta(days=1)
    matches = Match.query.filter(
        Match.match_date >= selected_date,
        Match.match_date < next_date
    ).order_by(Match.match_date).all()

    meta_tags = generate_meta_tags(
        title="Lịch Thi Đấu Bóng Đá | Kèo Sư",
        description="Xem lịch thi đấu bóng đá hôm nay và những ngày tới.",
        keywords="lịch thi đấu bóng đá, lịch thi đấu hôm nay"
    )
    return render_template('lich-thi-dau.html', matches=matches, selected_date=selected_date, meta_tags=meta_tags)


@app.route('/ty-so-truc-tiep')
def ty_so_truc_tiep():
    meta_tags = generate_meta_tags(
        title="Tỷ Số Trực Tiếp | Kèo Sư",
        description="Theo dõi tỷ số trực tiếp bóng đá tất cả các giải đấu.",
        keywords="tỷ số trực tiếp, kết quả bóng đá"
    )
    return render_template('ty-so-truc-tiep.html', meta_tags=meta_tags)

@app.route('/bai-viet/<slug>')
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, published=True).first_or_404()
    article.views += 1
    db.session.commit()

    related = Article.query.filter(
        Article.category_id == article.category_id,
        Article.id != article.id,
        Article.published == True
    ).limit(3).all()

    meta_tags = generate_meta_tags(
        title=article.meta_title or article.title,
        description=article.meta_description or article.get_excerpt(160),
        keywords=article.meta_keywords or f"{article.title}, {article.category.name}"
    )
    return render_template('article.html', article=article, related_articles=related, meta_tags=meta_tags)


@app.route('/chuyen-muc/<slug>')
@app.route('/chuyen-muc/<slug>/<int:page>')
def category_articles(slug, page=1):
    category = Category.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True)\
        .order_by(desc(Article.created_at))\
        .paginate(page=page, per_page=10, error_out=False)

    meta_tags = generate_meta_tags(
        title=f"{category.name} | Kèo Sư",
        description=category.description or f"Tất cả bài viết về {category.name}",
        keywords=f"{category.name}, {category.slug}"
    )
    return render_template('category.html', category=category, articles=articles, meta_tags=meta_tags)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if query:
        articles = Article.query.filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.content.ilike(f"%{query}%")
            ),
            Article.published == True
        ).order_by(desc(Article.created_at)).paginate(page=page, per_page=10, error_out=False)
    else:
        articles = []

    meta_tags = generate_meta_tags(
        title=f"Tìm kiếm: {query} | Kèo Sư" if query else "Tìm kiếm | Kèo Sư",
        description=f"Kết quả tìm kiếm cho '{query}'" if query else "Tìm kiếm bài viết",
        keywords=f"tìm kiếm, {query}" if query else "tìm kiếm"
    )
    return render_template('search.html', articles=articles, query=query, meta_tags=meta_tags)
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


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_articles = Article.query.count()
    return render_template('dashboard.html', total_articles=total_articles)


@app.route('/admin/create-article', methods=['GET', 'POST'])
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
            meta_title=form.meta_title.data,
            meta_description=form.meta_description.data,
            meta_keywords=form.meta_keywords.data,
            created_at=datetime.utcnow()
        )
        article.slug = article.generate_slug()

        # Đảm bảo slug là duy nhất
        original_slug = article.slug
        counter = 1
        while Article.query.filter_by(slug=article.slug).first():
            article.slug = f"{original_slug}-{counter}"
            counter += 1

        db.session.add(article)
        db.session.commit()
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('article_detail', slug=article.slug))

    return render_template('admin/create_article.html', form=form)


@app.route('/admin/articles')
@login_required
def manage_articles():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(desc(Article.created_at))\
        .paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/manage_articles.html', articles=articles)
@app.route('/sitemap.xml')
def sitemap():
    pages = []

    static_pages = [
        {'url': url_for('index'), 'priority': '1.0'},
        {'url': url_for('keo_thom'), 'priority': '0.9'},
        {'url': url_for('lich_thi_dau'), 'priority': '0.8'},
        {'url': url_for('ty_so_truc_tiep'), 'priority': '0.8'},
        {'url': url_for('admin_login'), 'priority': '0.3'},
    ]

    # Thêm các trang tĩnh vào danh sách
    for page in static_pages:
        pages.append({
            'url': page['url'],
            'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
            'priority': page['priority']
        })

    # Thêm các bài viết đã publish
    articles = Article.query.filter_by(published=True).all()
    for article in articles:
        pages.append({
            'url': url_for('article_detail', slug=article.slug, _external=True),
            'lastmod': article.updated_at.strftime('%Y-%m-%d') if article.updated_at else '',
            'priority': '0.7'
        })

    # Render XML từ template
    xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response
__all__ = ['main_bp']

