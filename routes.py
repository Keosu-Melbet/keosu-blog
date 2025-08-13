from flask import Flask, render_template, request

app = Flask(__name__)

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Tìm kiếm
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Xử lý tìm kiếm ở đây
    return render_template('search.html', query=query)

# Route động cho chuyên mục
@app.route('/<slug>')
def category_page(slug):
    # Bạn có thể kiểm tra slug và render template tương ứng
    return render_template('category.html', slug=slug)

# Chi tiết bài viết
@app.route('/bai-viet/<slug>')
def article_detail(slug):
    # Truy vấn bài viết theo slug
    return render_template('article_detail.html', slug=slug)

# Liên hệ
@app.route('/lien-he')
def lien_he():
    return render_template('lien_he.html')

# Đại lý MelBet
@app.route('/dai-ly-melbet')
def dai_ly_melbet():
    return render_template('dai_ly_melbet.html')
