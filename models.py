from flask_sqlalchemy import SQLAlchemy
from create_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


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

    @classmethod
    def encrypt_password(cls, pwd):

        """create user with encrypted password"""

        # Take the user's entered password, encrypt it and return the encrypted version
        hashed = bcrypt.generate_password_hash(pwd)

        # bcrypt returns a byte string, need to convert to standard utf8 string
        hashed_utf8 = hashed.decode("utf8")
        return hashed_utf8

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate the credentials of user attempting to log in
        returns User if valid, False if not"""

        # Query first user searched by entered name (user names are unique so there will
        # be 1 or 0 results)
        user = User.query.filter_by(username=username).first()

        # if a user is found AND the entered password gets encrypted the same as stored
        # password, return user class
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

    def __repr__(self):
        return f"{self.id} username: {self.username}, email: {self.email}"


class Feedback(db.Model):
    """Feed Back"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey("users.username"), nullable=False)

    users = db.relationship(User, backref="feedback")
