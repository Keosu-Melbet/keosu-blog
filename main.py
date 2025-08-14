import os
from app import create_app  # hoặc từ đúng module bạn đặt

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
