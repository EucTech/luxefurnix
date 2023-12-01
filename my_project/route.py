from flask import render_template, url_for, flash, redirect, request, abort
from my_project import app, db, bcrypt
from my_project.forms import SignupForm, LoginForm
from my_project.models import User, Product, Category
from flask_login import login_user, current_user, logout_user


with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/home")
def home():
    product = Product()
    category = Category()
    return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """This the route for signup"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    """This the route for login"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # To check if the form is validate when submit is clicked
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # Password is correct
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check email and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/description", methods=['GET', 'POST'])
def description():
    """This is the route for description"""
    return render_template('description.html')
