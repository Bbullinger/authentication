from flask_sqlalchemy import SQLAlchemy
from create_app import app


def connect_db(app):
    db = SQLAlchemy(app)
    db.app = app
    db.init_app(app)

    with app.app_context():
        db.create_all()
        return db


db = connect_db(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))

    def __repr__(self):
        return f"{self.id} username: {self.username}, email: {self.email}"
