# seed.py
from core import create_app, db
from models import Category

app = create_app()

def seed_default_categories():
    default_categories = [
        {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
        {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
        {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
        {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
        {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
    ]

    with app.app_context():
        db.create_all()
        created = False
        for cat_data in default_categories:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                db.session.add(Category(**cat_data))
                created = True

        if created:
            db.session.commit()
            print("✅ Đã tạo chuyên mục mặc định.")
        else:
            print("ℹ️ Chuyên mục đã tồn tại.")

if __name__ == "__main__":
    seed_default_categories()
