import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from my_project import app, db, bcrypt
from my_project.forms import SignupForm, LoginForm, UploadProductForm, ReviewForm
from my_project.models import User, Product, Category, Review
from flask_login import login_user, current_user, logout_user, login_required


with app.app_context():
    db.create_all()


    # category1 = Category(category_name="Table")
    # category2 = Category(category_name="Bed")
    # category3 = Category(category_name="Chair")
    # category4 = Category(category_name="Sofa")
    # category5 = Category(category_name="Cabinet")
    # db.session.add(category1)
    # db.session.add(category2)
    # db.session.add(category3)
    # db.session.add(category4)
    # db.session.add(category5)
    # db.session.commit()

    # categories = Category.query.all()

    # for category in categories:
    #     db.session.delete(category)

    # db.session.commit()

    
@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("home.html", products=products, categories=categories)


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
    """Route for uploading products.

    This route renders a form for users to upload new products. The available
    product categories are dynamically fetched from the database, and for each
    category, a tuple containing its ID and name is created. These tuples are
    then converted to strings and assigned to the choices of the 'category' field
    in the form.

    Upon form submission, the uploaded product details, including the selected
    category ID, are processed and saved to the database. Additionally, a flash
    message is displayed to indicate a successful product upload.

    Returns:
        If the form submission is successful, the user is redirected to the home
        page. Otherwise, the form is rendered with the appropriate choices and
        validation errors.

    """
    form = UploadProductForm()
    form.category.choices = [(str(category.id), category.category_name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        image_filename = save_pic(form.product_image.data)

        product = Product(
            product_name=form.product_name.data,
            product_desc=form.product_desc.data,
            price="{:.2f}".format(form.price.data),
            color=form.color.data,
            product_images=image_filename,
            category_id=form.category.data
        )

        db.session.add(product)
        db.session.commit()
        flash('Product uploadded successfully', 'success')
        return redirect(url_for('home'))
    return render_template("upload_products.html", title='Upload Products', form=form)


@app.route("/products/<string:product_id>", methods=['GET'])
def product(product_id):
    """This is the route for viewimg products through their ID"""
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    review = ""
    existing_review = Review.query.filter_by(product_id=product.id).all()
    if existing_review:
        review = existing_review
    return render_template('description.html', title=product.product_name, product=product, form=form, review=review)


@app.route("/products/<string:product_id>", methods=['POST'])
@login_required
def submit_review(product_id):
    """This is the route for viewimg products and
        writing product reviews and submit
    """
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    review = ""

    # To fill the form with the current users info
    if current_user.is_authenticated:
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email


    if form.validate_on_submit():
        review = Review(
            fullname=form.fullname.data,
            email=form.email.data,
            review_text=form.review_text.data,
            rating=form.rating.data,
            user_id=current_user.id,
            product_id=product.id
        )

        db.session.add(review)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('description.html', title=product.product_name, product=product, review=review, form=form)
