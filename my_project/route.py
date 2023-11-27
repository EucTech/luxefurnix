from flask import render_template
from my_project import app


@app.route("/")
@app.route("/h")
def home():
    return render_template("layout.html")