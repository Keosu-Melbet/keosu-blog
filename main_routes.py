from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash
)
from sqlalchemy import or_, desc
from datetime import datetime, timedelta
from models import Article, Category, BettingOdd, Match
from seo_utils import generate_meta_tags, create_structured_data
from core import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured = Article.query.filter_by(published=True, featured=True).limit(3).all()
    recent = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(6).all()

    meta_tags = generate_meta_tags(
        title="Kèo Sư - Website Kèo Bóng Đá Chuyên Nghiệp",
        description="Kèo Sư cung cấp tỷ lệ kèo, soi kèo, mẹo cược bóng đá chính xác.",
        keywords=["kèo bóng đá", "tỷ lệ kèo", "soi kèo"]
    )

    structured_data = create_structured_data("WebSite", {
        "name": "Kèo Sư",
        "url": request.url,
        "description": meta_tags["description"]
    })

    return render_template('index.html',
        featured_articles=featured,
        recent_articles=recent,
        meta_tags=meta_tags,
        structured_data=structured_data
    )

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        data = supabase.table("admins").select("*").eq("email", email).eq("password", password).execute()
        if data.data:
            session['user'] = email
            return redirect('/dashboard')
        else:
            return "Sai thông tin đăng nhập", 401

    return render_template('login.html')

@main_bp.route("/test")
def test():
    data = supabase.table("admins").select("*").execute()
    return str(data.data)

@main_bp.route('/keo-thom')
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
        keywords=["kèo thơm hôm nay", "tỷ lệ kèo"]
    )

    structured_data = create_structured_data("CollectionPage", {
        "name": "Kèo Thơm",
        "description": meta_tags["description"],
        "url": request.url
    })

    return render_template('keo-thom.html', odds=odds, meta_tags=meta_tags, structured_data=structured_data)

@main_bp.route('/lich-thi-dau')
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
        keywords=["lịch thi đấu bóng đá", "lịch thi đấu hôm nay"]
    )

    structured_data = create_structured_data("Event", {
        "name": "Lịch Thi Đấu",
        "startDate": str(selected_date),
        "description": meta_tags["description"],
        "url": request.url
    })

    return render_template('lich-thi-dau.html',
        matches=matches,
        selected_date=selected_date,
        meta_tags=meta_tags,
        structured_data=structured_data
    )

@main_bp.route('/ty-so-truc-tiep')
def ty_so_truc_tiep():
    meta_tags = generate_meta_tags(
        title="Tỷ Số Trực Tiếp | Kèo Sư",
        description="Theo dõi tỷ số trực tiếp bóng đá tất cả các giải đấu.",
        keywords=["tỷ số trực tiếp", "kết quả bóng đá"]
    )

    structured_data = create_structured_data("LiveBlogPosting", {
        "headline": meta_tags["title"],
        "description": meta_tags["description"],
        "url": request.url
    })

    return render_template('ty-so-truc-tiep.html',
        meta_tags=meta_tags,
        structured_data=structured_data
    )

@main_bp.route('/bai-viet/<slug>')
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
        keywords=article.meta_keywords or f"{article.title}, {article.category.name}",
        image=article.image,
        url=request.url
    )

    structured_data = create_structured_data("Article", {
        "title": article.title,
        "description": meta_tags["description"],
        "image": article.image,
        "author": "Kèo Sư",
        "published": str(article.created_at.date()),
        "updated": str(article.updated_at.date()) if article.updated_at else str(article.created_at.date()),
        "url": request.url
    })

    return render_template('article.html',
        article=article,
        related_articles=related,
        meta_tags=meta_tags,
        structured_data=structured_data
    )

@main_bp.route('/chuyen-muc/<slug>')
@main_bp.route('/chuyen-muc/<slug>/<int:page>')
def category_articles(slug, page=1):
    category = Category.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True)\
        .order_by(desc(Article.created_at))\
        .paginate(page=page, per_page=10, error_out=False)

    meta_tags = generate_meta_tags(
        title=f"{category.name} | Kèo Sư",
        description=category.description or f"Tất cả bài viết về {category.name}",
        keywords=[category.name, category.slug],
        url=request.url
    )

    structured_data = create_structured_data("CollectionPage", {
        "name": category.name,
        "description": meta_tags["description"],
        "url": request.url
    })

    return render_template('category.html',
        category=category,
        articles=articles,
        meta_tags=meta_tags,
        structured_data=structured_data
    )

@main_bp.route('/search')
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
        keywords=["tìm kiếm", query] if query else ["tìm kiếm"],
        url=request.url
    )

    structured_data = create_structured_data("SearchResultsPage", {
        "name": "Kết quả tìm kiếm",
        "description": meta_tags["description"],
        "url": request.url
    })

    return render_template('search.html',
        articles=articles,
        query=query,
        meta_tags=meta_tags,
        structured_data=structured_data
    )
