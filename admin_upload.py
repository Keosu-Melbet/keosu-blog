from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from models import Article
from core import create_app, db

app = create_app()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/upload-image/<int:id>', methods=['POST'])
def admin_upload_image(id):
    if 'image' not in request.files:
        flash('Không có file ảnh')
        return redirect(url_for('admin_edit_article', id=id))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Upload thành công')
        return redirect(url_for('admin_edit_article', id=id))
    else:
        flash('Định dạng file không hợp lệ')
        return redirect(url_for('admin_edit_article', id=id))

    
    file = request.files['image']
    if file.filename == '':
        flash('Chưa chọn file')
        return redirect(url_for('admin_edit_article', id=id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        article = Article.query.get_or_404(id)
        article.featured_image = filepath
        db.session.commit()
        
        flash('Đã cập nhật ảnh đại diện')
        return redirect(url_for('admin_edit_article', id=id))
    
    flash('File không hợp lệ')
    return redirect(url_for('admin_edit_article', id=id))
