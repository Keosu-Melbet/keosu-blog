def generate_meta_tags(
    title,
    description,
    keywords=None,
    image=None,
    url=None,
    site_name="Kèo Sư",
    type="website",
    twitter_handle="@keosu"
):
    """🔍 Generate meta tags for SEO, Open Graph, and Twitter Cards"""
    image = image or "/static/images/logo.svg"
    keywords = ", ".join(keywords) if isinstance(keywords, list) else (keywords or "")
    url = url or ""

    return {
        # Basic
        "title": title,
        "description": description,
        "keywords": keywords,

        # Open Graph
        "og:title": title,
        "og:description": description,
        "og:image": image,
        "og:url": url,
        "og:site_name": site_name,
        "og:type": type,

        # Twitter Card
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": image,
        "twitter:site": twitter_handle
    }
def create_structured_data(page_type, data):
    """📦 Create structured data for rich snippets (JSON-LD)"""
    structured = {
        "@context": "https://schema.org",
        "@type": page_type
    }

    # Auto-enhance for common types
    if page_type == "Article":
        structured.setdefault("headline", data.get("title"))
        structured.setdefault("image", data.get("image"))
        structured.setdefault("author", {
            "@type": "Person",
            "name": data.get("author", "Kèo Sư")
        })
        structured.setdefault("publisher", {
            "@type": "Organization",
            "name": "Kèo Sư",
            "logo": {
                "@type": "ImageObject",
                "url": "/static/images/logo.svg"
            }
        })
        structured.setdefault("datePublished", data.get("published"))
        structured.setdefault("dateModified", data.get("updated", data.get("published")))

    structured.update(data)
    return structured
