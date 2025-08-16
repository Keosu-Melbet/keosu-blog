from markupsafe import Markup
import json

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

def render_meta_tags(meta_tags):
    """🧩 Render meta tags as HTML for Flask templates"""
    lines = []

    if "title" in meta_tags:
        lines.append(f"<title>{meta_tags['title']}</title>")
    if "description" in meta_tags:
        lines.append(f'<meta name="description" content="{meta_tags["description"]}">')
    if "keywords" in meta_tags:
        lines.append(f'<meta name="keywords" content="{meta_tags["keywords"]}">')

    for key, value in meta_tags.items():
        if key.startswith("og:"):
            lines.append(f'<meta property="{key}" content="{value}">')
        elif key.startswith("twitter:"):
            lines.append(f'<meta name="{key}" content="{value}">')

    return Markup("\n".join(lines))

def render_structured_data(structured_data):
    """🧠 Render structured data as JSON-LD script"""
    return Markup(f'<script type="application/ld+json">\n{json.dumps(structured_data, indent=2)}\n</script>')
