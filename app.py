import os
import logging
from datetime import datetime
from core import create_app, db
from models import Category

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)

# 🚀 Tạo Flask app từ core.py
app = create_app()

# 📅 Template global: năm hiện tại
@app.template_global()
def get_current_year():
    return datetime.now().year

# 🧱 Khởi tạo dữ liệu mặc định (chuyên mục)
with app.app_context():
    default_categories = [
        {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
        {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
        {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
        {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
        {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
    ]

    for cat_data in default_categories:
        if not Category.query.filter_by(slug=cat_data['slug']).first():
            db.session.add(Category(**cat_data))

    try:
        db.session.commit()
        app.logger.info("✅ Đã tạo chuyên mục mặc định.")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"❌ Lỗi khi tạo chuyên mục mặc định: {e}")

# 🏃 Chạy ứng dụng
if __name__ == "__main__":
    app.run(debug=True)
