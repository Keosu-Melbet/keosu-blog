from core import db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Admin, Article, Category, BettingOdd, Match
from forms import ArticleForm, ContactForm, SearchForm
from werkzeug.security import check_password_hash
from seo_utils import generate_meta_tags
from sqlalchemy import or_, desc
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

@app.route('/')
def index():
    """Homepage"""
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

@app.route('/keo-thom')
def keo_thom():
    """Kèo thơm hôm nay page"""
    # Get today's betting odds
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    odds = BettingOdd.query.filter(
        BettingOdd.match_date >= today,
        BettingOdd.match_date < tomorrow
    ).all()
    
    meta_tags = generate_meta_tags(
        title="Kèo Thơm Hôm Nay - Tỷ Lệ Kèo Chính Xác | Kèo Sư",
        description="Cập nhật kèo thơm hôm nay, tỷ lệ kèo bóng đá chính xác từ các nhà cái uy tín. Phân tích chuyên sâu từ Kèo Sư.",
        keywords="kèo thơm hôm nay, tỷ lệ kèo hôm nay, kèo bóng đá"
    )
    
    return render_template('keo-thom.html', odds=odds, meta_tags=meta_tags)

@app.route('/lich-thi-dau')
def lich_thi_dau():
    """Lịch thi đấu page"""
    date_str = request.args.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()
    
    next_date = selected_date + timedelta(days=1)
    matches = Match.query.filter(
        Match.match_date >= selected_date,
        Match.match_date < next_date
    ).order_by(Match.match_date).all()
    
    meta_tags = generate_meta_tags(
        title="Lịch Thi Đấu Bóng Đá Hôm Nay | Kèo Sư",
        description="Xem lịch thi đấu bóng đá hôm nay và những ngày tới. Cập nhật liên tục từ các giải hàng đầu thế giới.",
        keywords="lịch thi đấu bóng đá, lịch thi đấu hôm nay"
    )
    
    return render_template('lich-thi-dau.html', 
                         matches=matches, 
                         selected_date=selected_date,
                         meta_tags=meta_tags)

@app.route('/ty-so-truc-tiep')
def ty_so_truc_tiep():
    """Tỷ số trực tiếp page"""
    meta_tags = generate_meta_tags(
        title="Tỷ Số Trực Tiếp Bóng Đá | Kèo Sư",
        description="Theo dõi tỷ số trực tiếp bóng đá tất cả các giải đấu. Cập nhật nhanh chóng và chính xác.",
        keywords="tỷ số trực tiếp, kết quả bóng đá trực tiếp"
    )
    
    return render_template('ty-so-truc-tiep.html', meta_tags=meta_tags)

@app.route('/soi-keo')
@app.route('/soi-keo/<int:page>')
def soi_keo(page=1):
    """Soi kèo page"""
    category = Category.query.filter_by(slug='soi-keo').first()
    if not category:
        flash('Chuyên mục không tồn tại', 'error' )
        return redirect(url_for('index'))
    
    articles = Article.query.filter_by(category_id=category.id, published=True)\
                          .order_by(desc(Article.created_at))\
                          .paginate(page=page, per_page=10, error_out=False)
    
    meta_tags = generate_meta_tags(
        title="Soi Kèo Bóng Đá Chuyên Nghiệp | Kèo Sư",
        description="Soi kèo bóng đá chuyên nghiệp, phân tích chi tiết các trận đấu. Tỷ lệ thắng cao từ chuyên gia Kèo Sư.",
        keywords="soi kèo bóng đá, phân tích kèo, dự đoán kết quả"
    )
    
    return render_template('soi-keo.html', 
                         articles=articles, 
                         category=category,
                         meta_tags=meta_tags)

@app.route('/meo-cuoc')
@app.route('/meo-cuoc/<int:page>')
def meo_cuoc(page=1):
    """Mẹo cược page"""
    category = Category.query.filter_by(slug='meo-cuoc').first()
    if not category:
        flash('Chuyên mục không tồn tại', 'error')
        return redirect(url_for('index'))
    
    articles = Article.query.filter_by(category_id=category.id, published=True)\
                          .order_by(desc(Article.created_at))\
                          .paginate(page=page, per_page=10, error_out=False)
    
    meta_tags = generate_meta_tags(
        title="Mẹo Cược Bóng Đá Hay Nhất | Kèo Sư",
        description="Chia sẻ mẹo cược bóng đá hiệu quả, kinh nghiệm chơi kèo từ các chuyên gia hàng đầu.",
        keywords="mẹo cược bóng đá, kinh nghiệm chơi kèo, cách chơi kèo"
    )
    
    return render_template('meo-cuoc.html', 
                         articles=articles, 
                         category=category,
                         meta_tags=meta_tags)

@app.route('/tin-tuc')
@app.route('/tin-tuc/<int:page>')
def tin_tuc(page=1):
    """Tin tức page"""
    category = Category.query.filter_by(slug='tin-tuc').first()
    if not category:
        flash('Chuyên mục không tồn tại', 'error')
        return redirect(url_for('index'))
    
    articles = Article.query.filter_by(category_id=category.id, published=True)\
                          .order_by(desc(Article.created_at))\
                          .paginate(page=page, per_page=10, error_out=False)
    
    meta_tags = generate_meta_tags(
        title="Tin Tức Bóng Đá Mới Nhất | Kèo Sư",
        description="Cập nhật tin tức bóng đá mới nhất, thông tin chuyển nhượng, kết quả thi đấu từ khắp thế giới.",
        keywords="tin tức bóng đá, tin bóng đá mới nhất"
    )
    
    return render_template('tin-tuc.html', 
                         articles=articles, 
                         category=category,
                         meta_tags=meta_tags)

@app.route('/dai-ly-melbet')
def dai_ly_melbet():
    """Đại lý MelBet page"""
    meta_tags = generate_meta_tags(
        title="Đại Lý MelBet - Chương Trình Affiliate Hấp Dẫn | Kèo Sư",
        description="Tham gia chương trình đại lý MelBet với hoa hồng cao, hỗ trợ 24/7. Cơ hội kinh doanh tuyệt vời.",
        keywords="đại lý MelBet, affiliate MelBet, kiếm tiền online"
    )
    
    return render_template('dai-ly-melbet.html', meta_tags=meta_tags)

@app.route('/lien-he', methods=['GET', 'POST'])
def lien_he():
    """Liên hệ page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Process contact form (could send email here)
        flash('Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi sớm nhất có thể.', 'success')
        return redirect(url_for('lien_he'))
    
    meta_tags = generate_meta_tags(
        title="Liên Hệ - Kèo Sư",
        description="Liên hệ với Kèo Sư để được tư vấn về kèo bóng đá, hợp tác kinh doanh và các dịch vụ khác.",
        keywords="liên hệ Kèo Sư, tư vấn kèo bóng đá"
    )
    
    return render_template('lien-he.html', form=form, meta_tags=meta_tags)

@app.route('/bai-viet/<slug>')
def article_detail(slug):
    """Article detail page"""
    article = Article.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Increment views
    article.views += 1
    db.session.commit()
    
    # Get related articles from same category
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

@app.route('/chuyen-muc/<slug>')
@app.route('/chuyen-muc/<slug>/<int:page>')
def category_articles(slug, page=1):
    """Category articles page"""
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

@app.route('/search')
def search():
    """Search articles"""
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

# -----------------------------
# 🔐 Admin Routes
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
        counter = 1
        original_slug = article.slug
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

# -----------------------------
# ⚙️ SEO Routes
# -----------------------------
@app.route('/sitemap.xml')
def sitemap():
    pages = []

    static_pages = [
        {'url': url_for('index'), 'priority': '1.0'},
        {'url': url_for('keo_thom'), 'priority': '0.9'},
        {'url': url_for('soi_keo'), 'priority': '0.9'},
        {'url': url_for('meo_cuoc'), 'priority': '0.8'},
        {'url': url_for('tin_tuc'), 'priority': '0.8'},
        {'url': url_for('lich_thi_dau'), 'priority': '0.7'},
        {'url': url_for('ty_so_truc_tiep'), 'priority': '0.7'},
        {'url': url_for('dai_ly_melbet'), 'priority': '0.6'},
        {'url': url_for('lien_he'), 'priority': '0.5'},
    ]

    articles = Article.query.filter_by(published=True).all()
    for article in articles:
        pages.append({
            'url': url_for('article_detail', slug=article.slug),
            'lastmod': article.updated_at.strftime('%Y-%m-%d') if article.updated_at else '',
            'priority': '0.8'
        })

    categories = Category.query.all()
    for category in categories:
        pages.append({
            'url': url_for('category_articles', slug=category.slug),
            'priority': '0.6'
        })

    pages.extend(static_pages)

    response = make_response(render_template('sitemap.xml', pages=pages))
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def robots():
    response = make_response(render_template('robots.txt'))
    response.headers['Content-Type'] = 'text/plain'
    return response

# -----------------------------
# 🌍 Context Processors
# -----------------------------
@app.context_processor
def inject_globals():
    categories = Category.query.all()
    search_form = SearchForm()
    return {
        'categories': categories,
        'search_form': search_form
    }

# -----------------------------
# ❌ Error Handlers
# -----------------------------
@app.errorhandler(404)
def not_found_error(error):
    meta_tags = generate_meta_tags(
        title="Trang không tồn tại | Kèo Sư",
        description="Trang bạn tìm kiếm không tồn tại.",
        keywords="404, không tìm thấy"
    )
    return render_template('404.html', meta_tags=meta_tags), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    meta_tags = generate_meta_tags(
        title="Lỗi hệ thống | Kèo Sư",
        description="Đã xảy ra lỗi hệ thống.",
        keywords="500, lỗi hệ thống"
    )
    return render_template('500.html', meta_tags=meta_tags), 500

# -----------------------------
# 🚀 Run App
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
