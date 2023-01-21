from flask import Flask, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User
from create_app import app


@app.route("/")
def home_page():
    return render_template("index.html")
