from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import db
from models.user import User
from models.subject import Subject



auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )


        db.session.add(new_user)
        db.session.flush()

        default_subjects = [
            "Python", "HTML", "CSS", "JavaScript", "PHP",
            "SQL", "Flask", "Django", "C", "C++",
            "Java", "React", "Bootstrap"
        ]

        for subject_name in default_subjects:
            subject = Subject(
                name=subject_name,
                description="",
                user_id=new_user.id
            )
            db.session.add(subject)

        db.session.commit()


        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard.dashboard_home"))

        flash("Invalid email or password.")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not check_password_hash(
            current_user.password,
            current_password
        ):
            flash("Current password is incorrect.")
            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match.")
            return redirect(url_for("auth.change_password"))

        if len(new_password) < 6:
            flash("New password must be at least 6 characters.")
            return redirect(url_for("auth.change_password"))

        current_user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Password changed successfully.")

        return redirect(url_for("auth.profile"))

    return render_template("change_password.html")



@auth.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":
        name = request.form["name"].strip()

        if not name:
            flash("Name cannot be empty.")
            return redirect(url_for("auth.edit_profile"))

        current_user.name = name
        db.session.commit()

        flash("Profile updated successfully.")
        return redirect(url_for("auth.profile"))

    return render_template("edit_profile.html", user=current_user)