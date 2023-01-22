from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Feedback
from create_app import app
from forms import RegisterForm, LoginForm, FeedbackForm


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.data["username"],
            # encrypt password and then save that to database, in place of user-entered
            # password
            password=User.encrypt_password(form.data["password"]),
            email=form.data["email"],
            first_name=form.data["first_name"],
            last_name=form.data["last_name"],
        )
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        flash(f"User {new_user.username} created.")
        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        password = form.data["password"]

        # User.authenticate returns the User class if validated, and false otherwise
        user = User.authenticate(username, password)
        if user:
            session["user_id"] = user.id
            return redirect("/")
        else:
            flash(f"Incorrect Username  and/or Password")
            return redirect("/secret")
    else:
        return render_template("login.html", form=form)


@app.route("/secret")
def success():
    if "user_id" not in session:
        flash("Please Log in first")
        return redirect("/")
    else:
        return "You Made it!"


@app.route("/logout")
def user_logout():
    if "user_id" in session:
        session.pop("user_id")
        flash("You have been successfully logged out.")
    else:
        flash("You have to be logged in to logout")
    return redirect("/")


@app.route("/users/<int:user_id>")
def user_show(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("user_show.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    if session["user_id"] == user_id:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted.")
    else:
        flash("You must be logged in to delete an account.")
    return redirect("/")


@app.route("/users/<int:user_id>/feedback/add", methods=["GET", "POST"])
def feedback_add(user_id):
    if "user_id" in session:
        form = FeedbackForm()
        current_user = User.query.get_or_404(user_id)
        if form.validate_on_submit():
            new_feedback = Feedback(
                title=form.data["title"],
                content=form.data["content"],
                username=current_user.username,
            )
            db.session.add(new_feedback)
            db.session.commit()
            flash("Feedback accepted.")
            return redirect("/")
        else:
            return render_template("feedback_add.html", form=form)
    else:
        flash("Please log in First.")
        return redirect("/")


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def feedback_edit(feedback_id):
    # check if user is logged in, if not, return user to homepage with error message
    if "user_id" in session:

        # Generate form, and obtain user's info and feedback's info
        form = FeedbackForm()
        feedback = Feedback.query.get_or_404(feedback_id)
        current_user = User.query.get_or_404(session["user_id"])

        # check if logged in user matches the user who created the feedback
        if feedback.username != current_user.username:
            flash("Only the owner of a post may alter it.")
            return redirect("/")

        # After checking a user is logged in, and the owner feedback, allow them to see the form and
        # update the existing feedback
        if form.validate_on_submit():
            feedback.title = form.data["title"]
            feedback.content = form.data["content"]
            db.session.commit()
            flash("Feedback updated.")
            return redirect("/")
        else:
            return render_template("feedback_edit.html", form=form)

    else:
        flash("You must be logged in to edit feedback.")
        return redirect("/")
