from models.database import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    tasks = db.relationship(
        "Task",
        backref="subject",
        lazy=True,
        cascade="all, delete-orphan"
    )

    user = db.relationship(
        "User",
        backref="subjects"
    )

    def __repr__(self):
        return f"<Subject {self.name}>"