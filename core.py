from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db, login_manager
from routes import main_bp
from models import Category
db.create_all()

def create_app():
    app = Flask(__name__)

    # Cấu hình ứng dụng
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keosu.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.secret_key = 'your-secret-key'  # Nên dùng biến môi trường khi deploy

    # Xử lý proxy headers (Render, Heroku, v.v.)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Đăng ký blueprint và khởi tạo dữ liệu
    with app.app_context():
        app.register_blueprint(main_bp)
        
        # Tạo chuyên mục mặc định nếu chưa có
        default_categories = [
            {'name': 'Kèo thơm', 'slug': 'keo-thom', 'description': 'Những kèo thơm hôm nay'},
            {'name': 'Soi kèo', 'slug': 'soi-keo', 'description': 'Phân tích và soi kèo trận đấu'},
            {'name': 'Mẹo cược', 'slug': 'meo-cuoc', 'description': 'Mẹo và kinh nghiệm cược bóng đá'},
            {'name': 'Tin tức', 'slug': 'tin-tuc', 'description': 'Tin tức bóng đá mới nhất'},
            {'name': 'Lịch thi đấu', 'slug': 'lich-thi-dau', 'description': 'Lịch thi đấu các giải'},
        ]
        for cat in default_categories:
            if not Category.query.filter_by(slug=cat['slug']).first():
                db.session.add(Category(**cat))
        db.session.commit()

    return app

