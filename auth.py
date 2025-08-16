from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import login_manager
from models import Admin  # Sử dụng model Admin để đăng nhập
from werkzeug.security import check_password_hash

# 📦 Tạo blueprint cho auth
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# 🔐 Định nghĩa cách Flask-Login tải người dùng từ session
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# 🧑 Route đăng nhập
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash("✅ Đăng nhập thành công!", "success")
            return redirect(url_for("admin.dashboard"))  # hoặc trang chính của admin
        else:
            flash("❌ Sai tên đăng nhập hoặc mật khẩu.", "danger")

    return render_template("login.html")

# 🚪 Route đăng xuất
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 Bạn đã đăng xuất.", "info")
    return redirect(url_for("main.index"))
