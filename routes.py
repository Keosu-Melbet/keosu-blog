from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response, session
from extensions import db
from models import Article, Category, BettingOdd, Match, User
from forms import ArticleForm, ContactForm, SearchForm
from seo_utils import generate_meta_tags
from datetime import datetime, timedelta
from sqlalchemy import or_, desc
from functools import wraps

bp = Blueprint('main', __name__)

# Trang chủ
@bp.route('/')
def index():
    featured_articles = Article.query.filter_by(published=True, featured=True).limit(3).all()
    recent_articles = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(6).all()
    
    meta_tags = generate_meta_tags(
        title="Kèo Sư - Website Kèo Bóng Đá Chuyên Nghiệp",
        description="Kèo Sư cung cấp tỷ lệ kèo, soi kèo, mẹo cược bóng đá chính xác. Đối tác chính thức MelBet Việt Nam.",
        keywords="kèo bóng đá, tỷ lệ kèo, soi kèo, mẹo cược, MelBet"
    )
    
    return render_template('index.html', 
                           featured_articles=featured_articles,
                           recent_articles=recent_articles,
                           meta_tags=meta_tags)

# Chi tiết bài viết
@bp.route('/bai-viet/<slug>')
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, published=True).first_or_404()
    article.views += 1
    db.session.commit()
    
    related_articles = Article.query.filter(
        Article.category_id == article.category_id,
        Article.id != article.id,
        Article.published == True
    ).limit(3).all()
    
    meta_tags = generate_meta_tags(
        title=article.meta_title or article.title,
        description=article.meta_description or article.get_excerpt(160),
        keywords=article.meta_keywords or f"{article.title}, {article.category.name}"
    )
    
    return render_template('article.html', 
                           article=article, 
                           related_articles=related_articles,
                           meta_tags=meta_tags)

# Chuyên mục bài viết
@bp.route('/chuyen-muc/<slug>')
@bp.route('/chuyen-muc/<slug>/<int:page>')
def category_articles_vn(slug, page=1):
    category = Category.query.filter_by(slug=slug).first_or_404()
    
    articles = Article.query.filter_by(category_id=category.id, published=True)\
                            .order_by(desc(Article.created_at))\
                            .paginate(page=page, per_page=10, error_out=False)
    
    meta_tags = generate_meta_tags(
        title=f"{category.name} | Kèo Sư",
        description=category.description or f"Tất cả bài viết về {category.name}",
        keywords=f"{category.name}, {category.slug}"
    )
    
    return render_template('category.html', 
                           category=category, 
                           articles=articles,
                           meta_tags=meta_tags)

# Kèo thơm hôm nay
@bp.route('/keo-thom')
def keo_thom():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    odds = BettingOdd.query.filter(
        BettingOdd.match_date >= today,
        BettingOdd.match_date < tomorrow
    ).all()
    
    meta_tags = generate_meta_tags(
        title="Kèo Thơm Hôm Nay - Tỷ Lệ Kèo Chính Xác | Kèo Sư",
        description="Cập nhật kèo thơm hôm nay, tỷ lệ kèo bóng đá chính xác từ các nhà cái uy tín.",
        keywords="kèo thơm hôm nay, tỷ lệ kèo hôm nay"
    )
    
    return render_template('keo-thom.html', odds=odds, meta_tags=meta_tags)

# Lịch thi đấu
@bp.route('/lich-thi-dau')
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
        title="Lịch Thi Đấu Bóng Đá Hôm Nay | Kèo Sư",
        description="Xem lịch thi đấu bóng đá hôm nay và những ngày tới.",
        keywords="lịch thi đấu bóng đá, lịch thi đấu hôm nay"
    )
    
    return render_template('lich-thi-dau.html', 
                           matches=matches, 
                           selected_date=selected_date,
                           meta_tags=meta_tags)

# Tìm kiếm bài viết
@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        articles = Article.query.filter(
            or_(
                Article.title.contains(query),
                Article.content.contains(query)
            ),
            Article.published == True
        ).order_by(desc(Article.created_at))\
         .paginate(page=page, per_page=10, error_out=False)
    else:
        articles = Article.query.filter_by(published=False).paginate(page=1, per_page=0, error_out=False)
    
    meta_tags = generate_meta_tags(
        title=f"Tìm kiếm: {query} | Kèo Sư" if query else "Tìm kiếm | Kèo Sư",
        description=f"Kết quả tìm kiếm cho '{query}'" if query else "Tìm kiếm bài viết",
        keywords=f"tìm kiếm, {query}" if query else "tìm kiếm"
    )
    
    return render_template('search.html', 
                           articles=articles, 
                           query=query,
                           meta_tags=meta_tags)

# Admin login
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_admin:
            session['admin_logged_in'] = True
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Sai thông tin đăng nhập hoặc không có quyền truy cập.')
    return render_template('admin/login.html')

@bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    articles = Article.query.order_by(desc(Article.created_at)).all()
    return render_template('admin/dashboard.html', articles=articles)

@bp.route('/admin/create-article', methods=['GET', 'POST'])
@admin_required
def create_article():
    form = ArticleForm()
    
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
            meta_keywords=form.meta_keywords.data
        )
        
        article.slug = article.generate_slug()
        counter = 1
        original_slug = article.slug
        while Article.query.filter_by(slug=article.slug).first():
            article.slug = f"{original_slug}-{counter}"
            counter += 1
        
        db.session.add(article)
        db.session.commit()
        
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('main.article_detail', slug=article.slug))
    
    return render_template('admin/create_article.html', form=form)

@bp.route('/admin/articles')
@admin_required
def manage_articles():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(desc(Article.created_at))\
                            .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/manage_articles.html', articles=articles)

@bp.route('/sitemap.xml')
def sitemap():
    pages = []
    static_pages = [
        {'url': url_for('main.index'), 'priority': '1.0'},
        {'url': url_for('main.keo_thom'), 'priority': '0.9'},
        {'url': url_for('main.lich_thi_dau'), 'priority': '0.8'},
        {'url': url_for('main.search'), 'priority': '0.7'},
        {'url': url_for('main.admin_login'), 'priority': '0.5'},
    ]
    
    articles = Article.query.filter_by(published=True).all()
    for article in articles:
        pages.append({
            'url': url_for('main.article_detail', slug=article.slug),
            'lastmod': article.updated_at.strftime('%Y-%m-%d'),
            'priority': '0.8'
        })
    
    categories = Category.query.all()
    for category in categories:
        pages.append({
            'url': url_for('main.category_articles_vn', slug=category.slug),
            'priority': '0.6'
        })
    
    pages.extend(static_pages)
    
    response = make_response(render_template('sitemap.xml', pages=pages))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/robots.txt')
def robots():
    response = make_response(render_template('robots.txt'))
    response.headers['Content-Type'] = 'text/plain'
    return response

@bp.app_context_processor
def inject_globals():
    categories = Category.query.all()
    search_form = SearchForm()
    return {
        'categories': categories,
        'search_form': search_form
    }

@bp.app_errorhandler(404)
def not_found_error(error):
    meta_tags = generate_meta_tags(
        title="Trang không tồn tại | Kèo Sư",
        description="Trang bạn tìm kiếm không tồn tại.",
        keywords="404, không tìm thấy"
    )
    return render_template('404.html', meta_tags=meta_tags), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    meta_tags = generate_meta_tags(
        title="Lỗi hệ thống | Kèo Sư",
        description="Đã xảy ra lỗi hệ thống.",
        keywords="500, lỗi hệ thống"
    )
    return render_template('500.html', meta_tags=meta_tags), 500
