import os
from app import create_app
from app import routes  # ✅ Import để Flask biết đến route

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
