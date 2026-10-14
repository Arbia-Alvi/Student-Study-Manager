from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required, current_user
from datetime import datetime
import json

from models.database import db
from models.task import Task
from models.subject import Subject


tasks = Blueprint("tasks", __name__)



@tasks.route("/tasks")
@login_required
def task_list():

    search = request.args.get("search", "").strip()
    priority = request.args.get("priority", "").strip()
    status = request.args.get("status", "").strip()
    sort_by = request.args.get("sort_by", "newest").strip()

    if sort_by not in ["newest", "due_date", "priority"]:
        sort_by = "newest"

    query = Task.query.join(Subject).filter(
        Subject.user_id == current_user.id
    )

    # Search by title or description
    if search:
        query = query.filter(
            db.or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    # Filter by priority
    if priority:
        query = query.filter(Task.priority == priority)

    # Filter by status
    if status == "completed":
        query = query.filter(Task.completed == True)
    elif status == "pending":
        query = query.filter(Task.completed == False)

    # Sort tasks
    if sort_by == "due_date":
        query = query.order_by(
            Task.due_date.is_(None),
            Task.due_date.asc()
        )
    elif sort_by == "priority":
        query = query.order_by(
            db.case(
                (Task.priority == "High", 1),
                (Task.priority == "Medium", 2),
                (Task.priority == "Low", 3),
                else_=4
            )
        )
    else:
        query = query.order_by(Task.id.desc())

    all_tasks = query.all()
    current_date = datetime.today().date()

    return render_template(
        "tasks.html",
        tasks=all_tasks,
        search=search,
        priority=priority,
        status=status,
        sort_by=sort_by,
        current_date=current_date
    )

@tasks.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():


    print("DEBUG SUBJECTS:", [(s.id, s.name, s.user_id) for s in Subject.query.all()])

    print("CURRENT USER ID:", current_user.id)

    subjects = Subject.query.filter_by(
        user_id=current_user.id
    ).all()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "").strip()
        due_date_text = request.form.get("due_date", "").strip()
        subject_id = request.form.get("subject_id", "").strip()

        # Title validation
        if not title:
            flash("Task title is required.")
            return render_template(
                "add_task.html",
                subjects=subjects
            )

        # Priority validation
        if priority not in ["Low", "Medium", "High"]:
            flash("Please select a valid priority.")
            return render_template(
                "add_task.html",
                subjects=subjects
            )

        # Subject validation
        if not subject_id.isdigit():
            flash("Please select a valid subject.")
            return render_template(
                "add_task.html",
                subjects=subjects
            )

        subject = Subject.query.filter_by(
            id=int(subject_id),
            user_id=current_user.id
        ).first()

        if not subject:
            flash("Please select a valid subject.")
            return render_template(
                "add_task.html",
                subjects=subjects
            )

        # Date validation
        due_date = None

        if due_date_text:

            try:
                due_date = datetime.strptime(
                    due_date_text,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                flash("Invalid due date.")
                return render_template(
                    "add_task.html",
                    subjects=subjects
                )

        try:

            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                subject_id=subject.id
            )

            db.session.add(task)
            db.session.commit()

            flash("Task added successfully!")

            return redirect(url_for("tasks.task_list"))

        except Exception:

            db.session.rollback()

            flash("Something went wrong while adding the task.")

    return render_template(
        "add_task.html",
        subjects=subjects
    )


@tasks.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    task = Task.query.join(Subject).filter(

    Task.id == task_id,
        Subject.user_id == current_user.id
    ).first_or_404()


    subjects = Subject.query.all()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "").strip()
        due_date_text = request.form.get("due_date", "").strip()
        subject_id = request.form.get("subject_id", "").strip()

        # Title validation
        if not title:
            flash("Task title is required.")
            return render_template(
                "edit_task.html",
                task=task,
                subjects=subjects
            )

        # Priority validation
        if priority not in ["Low", "Medium", "High"]:
            flash("Please select a valid priority.")
            return render_template(
                "edit_task.html",
                task=task,
                subjects=subjects
            )

        # Subject validation
        if not subject_id.isdigit():
            flash("Please select a valid subject.")
            return render_template(
                "edit_task.html",
                task=task,
                subjects=subjects
            )

        subject = db.session.get(Subject, int(subject_id))

        if not subject:
            flash("Selected subject does not exist.")
            return render_template(
                "edit_task.html",
                task=task,
                subjects=subjects
            )

        # Date validation
        due_date = None

        if due_date_text:

            try:
                due_date = datetime.strptime(
                    due_date_text,
                    "%Y-%m-%d"
                ).date()

            except ValueError:
                flash("Invalid due date.")
                return render_template(
                    "edit_task.html",
                    task=task,
                    subjects=subjects
                )

        try:

            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            task.subject_id = subject.id

            db.session.commit()

            flash("Task updated successfully!")

            return redirect(url_for("tasks.task_list"))

        except Exception:

            db.session.rollback()

            flash("Something went wrong while updating the task.")

    return render_template(
        "edit_task.html",
        task=task,
        subjects=subjects
    )




@tasks.route("/tasks/complete/<int:task_id>")
@login_required
def complete_task(task_id):

    task = Task.query.join(Subject).filter(
        Task.id == task_id,
        Subject.user_id == current_user.id
    ).first_or_404()

    task.completed = True

    db.session.commit()

    flash("Task marked as completed!")

    return redirect(url_for("tasks.task_list"))


@tasks.route("/tasks/delete/<int:task_id>")
@login_required
def delete_task(task_id):

    task = Task.query.join(Subject).filter(
        Task.id == task_id,
        Subject.user_id == current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully!")

    return redirect(url_for("tasks.task_list"))


@tasks.route("/tasks/export")
@login_required
def export_tasks():

    all_tasks = Task.query.all()

    data = []

    for task in all_tasks:

        data.append({
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": (
                task.due_date.strftime("%Y-%m-%d")
                if task.due_date else None
            ),
            "completed": task.completed,
            "subject": (
                task.subject.name
                if task.subject else None
            )
        })

    json_data = json.dumps(data, indent=4)

    return Response(
        json_data,
        mimetype="application/json",
        headers={
            "Content-Disposition":
            "attachment; filename=student_tasks.json"
        }
    )


@tasks.route("/tasks/import", methods=["POST"])
@login_required
def import_tasks():

    file = request.files.get("json_file")

    if not file or file.filename == "":
        flash("Please select a JSON file.")
        return redirect(url_for("tasks.task_list"))

    if not file.filename.lower().endswith(".json"):
        flash("Only JSON files are allowed.")
        return redirect(url_for("tasks.task_list"))

    try:

        data = json.load(file)

        if not isinstance(data, list):
            flash("Invalid JSON format. Expected a list of tasks.")
            return redirect(url_for("tasks.task_list"))

        imported_count = 0

        for item in data:

            if not isinstance(item, dict):
                continue

            title = str(item.get("title", "")).strip()

            if not title:
                continue

            description = str(
                item.get("description", "")
            ).strip()

            priority = item.get("priority", "Medium")

            if priority not in ["Low", "Medium", "High"]:
                priority = "Medium"

            subject_name = item.get("subject")

            if not subject_name:
                continue

            subject = Subject.query.filter_by(
                name=subject_name
            ).first()

            if not subject:
                continue

            due_date = None

            if item.get("due_date"):

                try:

                    due_date = datetime.strptime(
                        str(item["due_date"]),
                        "%Y-%m-%d"
                    ).date()

                except ValueError:

                    due_date = None

            completed = item.get("completed", False)

            if not isinstance(completed, bool):
                completed = False

            task = Task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                completed=completed,
                subject_id=subject.id
            )

            db.session.add(task)
            imported_count += 1

        db.session.commit()

        flash(
            f"{imported_count} task(s) imported successfully!"
        )

    except json.JSONDecodeError:

        db.session.rollback()

        flash("The uploaded file contains invalid JSON.")

    except Exception:

        db.session.rollback()

        flash("Something went wrong while importing the JSON file.")

    return redirect(url_for("tasks.task_list"))


@tasks.route("/api/tasks")
@login_required
def api_tasks():

    all_tasks = Task.query.all()

    data = []

    for task in all_tasks:

        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": (
                task.due_date.strftime("%Y-%m-%d")
                if task.due_date else None
            ),
            "completed": task.completed,
            "subject_id": task.subject_id
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "tasks": data
    })