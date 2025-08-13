import re
from datetime import datetime
from flask import url_for
from models import Article, Category

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    # Vietnamese character mapping
    vietnamese_map = {
        'à': 'a', 'á': 'a', 'ạ': 'a', 'ả': 'a', 'ã': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ậ': 'a', 'ẩ': 'a', 'ẫ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ặ': 'a', 'ẳ': 'a', 'ẵ': 'a',
        'è': 'e', 'é': 'e', 'ẹ': 'e', 'ẻ': 'e', 'ẽ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ệ': 'e', 'ể': 'e', 'ễ': 'e',
        'ì': 'i', 'í': 'i', 'ị': 'i', 'ỉ': 'i', 'ĩ': 'i',
        'ò': 'o', 'ó': 'o', 'ọ': 'o', 'ỏ': 'o', 'õ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ộ': 'o', 'ổ': 'o', 'ỗ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ợ': 'o', 'ở': 'o', 'ỡ': 'o',
        'ù': 'u', 'ú': 'u', 'ụ': 'u', 'ủ': 'u', 'ũ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ự': 'u', 'ử': 'u', 'ữ': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỵ': 'y', 'ỷ': 'y', 'ỹ': 'y',
        'đ': 'd',
        'À': 'A', 'Á': 'A', 'Ạ': 'A', 'Ả': 'A', 'Ã': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ậ': 'A', 'Ẩ': 'A', 'Ẫ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ặ': 'A', 'Ẳ': 'A', 'Ẵ': 'A',
        'È': 'E', 'É': 'E', 'Ẹ': 'E', 'Ẻ': 'E', 'Ẽ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ệ': 'E', 'Ể': 'E', 'Ễ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ị': 'I', 'Ỉ': 'I', 'Ĩ': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ọ': 'O', 'Ỏ': 'O', 'Õ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ộ': 'O', 'Ổ': 'O', 'Ỗ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ợ': 'O', 'Ở': 'O', 'Ỡ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ụ': 'U', 'Ủ': 'U', 'Ũ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ự': 'U', 'Ử': 'U', 'Ữ': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y',
        'Đ': 'D'
    }
    
    # Convert to lowercase
    slug = title.lower()
    
    # Replace Vietnamese characters
    for vn_char, en_char in vietnamese_map.items():
        slug = slug.replace(vn_char, en_char)
    
    # Replace special characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Ensure uniqueness
    original_slug = slug
    counter = 1
    while Article.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug

def create_sitemap():
    """Generate XML sitemap"""
    base_url = "https://keo-su-mel-bet.onrender.com"
    
    urls = []
    
    # Add static pages
    static_pages = [
        ('index', 1.0, 'daily'),
        ('keo_thom', 0.9, 'daily'),
        ('lich_thi_dau', 0.8, 'daily'),
        ('ty_so_truc_tiep', 0.8, 'daily'),
        ('soi_keo', 0.9, 'daily'),
        ('meo_cuoc', 0.8, 'weekly'),
        ('tin_tuc', 0.8, 'daily'),
        ('dai_ly_melbet', 0.7, 'monthly'),
        ('lien_he', 0.6, 'monthly'),
    ]
    
    for page, priority, changefreq in static_pages:
        urls.append({
            'loc': f"{base_url}{url_for(page)}",
            'priority': priority,
            'changefreq': changefreq,
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
    
    # Add articles
    articles = Article.query.filter_by(published=True).all()
    for article in articles:
        urls.append({
            'loc': f"{base_url}{url_for('article_detail', slug=article.slug)}",
            'priority': 0.8,
            'changefreq': 'weekly',
            'lastmod': article.updated_at.strftime('%Y-%m-%d')
        })
    
    # Add categories
    categories = Category.query.all()
    for category in categories:
        urls.append({
            'loc': f"{base_url}{url_for('category_articles', slug=category.slug)}",
            'priority': 0.7,
            'changefreq': 'daily',
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
    
    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml

def format_date(date, format='%d/%m/%Y'):
    """Format datetime object"""
    return date.strftime(format)

def truncate_text(text, length=100):
    """Truncate text to specified length"""
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + '...'
