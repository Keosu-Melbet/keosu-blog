from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from models import Admin

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.index"))  # hoặc dashboard
        else:
            flash("Sai thông tin đăng nhập.", "danger")
    return render_template("login.html")
