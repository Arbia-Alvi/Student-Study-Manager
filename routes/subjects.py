from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.database import db
from models.subject import Subject


subjects = Blueprint("subjects", __name__)



@subjects.route("/subjects")
@login_required
def subject_list():
    all_subjects = Subject.query.filter_by(
        user_id=current_user.id
    ).order_by(Subject.name).all()

    return render_template(
        "subjects.html",
        subjects=all_subjects
    )


@subjects.route("/subjects/add", methods=["GET", "POST"])
@login_required
def add_subject():

    if request.method == "POST":

        name = request.form["name"].strip()
        description = request.form["description"].strip()

        subject = Subject(
            name=name,
            description=description,
            user_id=current_user.id
        )

        db.session.add(subject)
        db.session.commit()

        return redirect(url_for("subjects.subject_list"))

    return render_template("add_subject.html")


@subjects.route("/subjects/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subject(id):

    subject = Subject.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        subject.name = request.form["name"].strip()
        subject.description = request.form["description"].strip()

        db.session.commit()

        return redirect(url_for("subjects.subject_list"))

    return render_template(
        "edit_subject.html",
        subject=subject
    )



@subjects.route("/subjects/delete/<int:id>", methods=["POST"])
@login_required
def delete_subject(id):

    subject = Subject.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(subject)
    db.session.commit()

    return redirect(url_for("subjects.subject_list"))