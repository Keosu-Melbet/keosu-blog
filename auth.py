from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from supabase_client import supabase
from models import Admin

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        result = supabase.table("admins").select("*").eq("email", email).single().execute()
        admin_data = result.data

        if admin_data and check_password_hash(admin_data["password"], password):
            # Nếu bạn dùng Flask-Login với model Admin
            admin = Admin.query.filter_by(email=email).first()
            if admin:
                login_user(admin)
                return redirect(url_for("admin.dashboard"))
            else:
                flash("Không tìm thấy tài khoản admin trong hệ thống.", "danger")
        else:
            flash("Sai thông tin đăng nhập.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
