from flask import render_template, url_for, flash, redirect
from my_project import app, db, bcrypt
from my_project.forms import SignupForm, LoginForm
from my_project.models import User


with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = SignupForm()
    # To check if the form is validate when submit is clicked
    if form.validate_on_submit():
        # To hash the password
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, email=
                    form.email.data, phone_number=form.phone_number.data, password=hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


