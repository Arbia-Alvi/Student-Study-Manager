from models.database import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.String(500))

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    due_date = db.Column(db.Date)

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Task {self.title}>"