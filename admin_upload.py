from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from core import app, db  # ✅ Import app và db từ core
from models import Article

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/upload-image/<int:id>', methods=['POST'])
def admin_upload_image(id):
    file = request.files.get('image')  # ✅ Lấy file đúng cách

    if not file or file.filename == '':
        flash('Chưa chọn file hoặc không có file ảnh')
        return redirect(url_for('admin_edit_article', id=id))

    if not allowed_file(file.filename):
        flash('Định dạng file không hợp lệ')
        return redirect(url_for('admin_edit_article', id=id))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # ✅ Cập nhật ảnh đại diện cho bài viết
    article = Article.query.get_or_404(id)
    article.featured_image = filepath
    db.session.commit()

    flash('Đã cập nhật ảnh đại diện')
    return redirect(url_for('admin_edit_article', id=id))
