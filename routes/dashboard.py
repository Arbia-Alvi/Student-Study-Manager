from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date

from models.database import db
from models.subject import Subject
from models.task import Task


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    user_subjects = Subject.query.filter_by(
        user_id=current_user.id
    ).all()

    subject_ids = [subject.id for subject in user_subjects]

    total_subjects = len(user_subjects)

    total_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids)
    ).count() if subject_ids else 0

    completed_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == True
    ).count() if subject_ids else 0

    pending_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == False
    ).count() if subject_ids else 0

    overdue_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == False,
        Task.due_date < date.today()
    ).count() if subject_ids else 0



    due_today_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == False,
        Task.due_date == date.today()
    ).count() if subject_ids else 0

    upcoming_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == False,
        Task.due_date > date.today()
    ).count() if subject_ids else 0



    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    recent_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids)
    ).order_by(
        Task.created_at.desc()
    ).limit(5).all() if subject_ids else []

    return render_template(
        "dashboard.html",
        user=current_user,
        total_subjects=total_subjects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        due_today_tasks=due_today_tasks,
        upcoming_tasks=upcoming_tasks,
        progress=progress,
        recent_tasks=recent_tasks
    )