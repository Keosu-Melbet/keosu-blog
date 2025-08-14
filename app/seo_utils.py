def generate_meta_tags(title, description, keywords=None, image=None, url=None):
    """Generate meta tags for SEO"""
    meta_tags = {
        'title': title,
        'description': description,
        'keywords': keywords or '',
        'image': image or '/static/images/logo.svg',
        'url': url or '',
        'site_name': 'Kèo Sư',
        'type': 'website'
    }
    return meta_tags

def create_structured_data(page_type, data):
    """Create structured data for rich snippets"""
    base_data = {
        "@context": "https://schema.org",
        "@type": page_type
    }
    base_data.update(data)
    return base_data
