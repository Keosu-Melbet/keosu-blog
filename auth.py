from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from models import Admin
from core import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = Admin.query.filter_by(email=email).first()

        if admin and admin.check_password(password):
            login_user(admin)
            flash("✅ Đăng nhập thành công!", "success")
            return redirect(url_for("main.index"))  # hoặc "dashboard" nếu bạn có route đó
        else:
            flash("❌ Sai thông tin đăng nhập.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")
