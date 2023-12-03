import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from my_project import app, db, bcrypt
from my_project.forms import SignupForm, LoginForm, UploadProductForm
from my_project.models import User, Product
from flask_login import login_user, current_user, logout_user, login_required


with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


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


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/images/products', picture_fn)

    # To resize the image before uploading
    output_size = (800, 800)
    i = Image.open(form_pic)
    i.thumbnail(output_size)

    i.save(pic_path)

    return picture_fn


@app.route("/upload_products", methods=['GET', 'POST'])
@login_required
def upload_products():
    """This is a route that uploads products"""
    form = UploadProductForm()
    if form.validate_on_submit():
        image_filename = save_pic(form.product_image.data)

        product = Product(
            product_name=form.product_name.data,
            product_desc=form.product_desc.data,
            price=form.price.data,
            color=form.color.data,
            product_images=image_filename,
            # category_id=
        )

        db.session.add(product)
        db.session.commit()
        flash('Product uploadded successfully', 'success')
        return redirect(url_for('home'))
    return render_template("upload_products.html", title='Upload Products', form=form)


@app.route("/products/<string:product_id>", methods=['GET', 'POST'])
def product(product_id):
    """This is the route for products"""
    product = Product.query.get_or_404(product_id)
    return render_template('description.html', title=product.product_name, product=product)
