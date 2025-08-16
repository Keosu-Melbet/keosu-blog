import os
import logging
from datetime import datetime
from core import create_app

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)

# 🚀 Tạo Flask app từ core.py
app = create_app()

# 📅 Template global: năm hiện tại
@app.template_global()
def get_current_year():
    return datetime.now().year

# 🏃 Chạy ứng dụng
if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
