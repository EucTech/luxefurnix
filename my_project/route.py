import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from my_project import app, db, bcrypt
from my_project.forms import SignupForm, LoginForm, UploadProductForm, ReviewForm, ShoppingCartForm
from my_project.models import User, Product, Category, Review, ShoppingCart
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm.exc import NoResultFound


with app.app_context():
    db.create_all()
    
    
    # c = Category(category_name="Table")
    # c1 = Category(category_name="Chair")
    # c2 = Category(category_name="Bed")
    # c3 = Category(category_name="Sofa")
    # c4 = Category(category_name="Cabinet")
    # db.session.add(c)
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    # db.session.add(c4)
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
            price=form.price.data,
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
        
    # To fill the form with the current users info
    if current_user.is_authenticated:
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
        
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
    
    return render_template('description.html', title=product.product_name, product=product, review=review, form=form, cart=cart)


@app.route("/shopping-cart", methods=['GET', 'POST', 'PUT'])
@login_required
def view_cart():
    """This a route to view for cart"""    
    cart = ShoppingCart.query.filter_by(user_id=current_user.id).all()
    
    # Make sure to load the associated product for each cart item
    for item in cart:
        item.product = Product.query.get_or_404(item.product_id)

        item.calculate_total()
        
    form = ShoppingCartForm()
    
    return render_template('shopping_cart.html', cart=cart, title='Shopping-cart', form=form)


@app.route("/add-to-cart/<string:product_id>", methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    """This a route for cart"""
    if current_user.is_authenticated:
        product = Product.query.get_or_404(product_id)
        try:
            cart = ShoppingCart.query.filter_by(
                user_id=current_user.id,
                product_id=product.id
            ).one()
        except NoResultFound:
            cart = ShoppingCart(
                user_id=current_user.id,
                product_id=product.id,
                quantity=1,
                total=product.price
            )

            db.session.add(cart)
            db.session.commit()            
        count_cart = ShoppingCart.query.filter_by(user_id=current_user.id).count()
        
    return jsonify({'message': 'Product added to cart!', 'count_cart': count_cart})
    # return render_template('description.html', count_cart=count_cart, cart=cart)


@app.route("/shopping-cart/<string:product_id>", methods=['POST', 'PUT'])
@login_required
def update_quantity(product_id):
    """This route updates the quantity of item in the cart"""
    if current_user.is_authenticated:
        quantity = request.form.get('quantity')
        
        if not quantity:
            abort(400, {'error': 'Quantity is missing'})
            
        cart = ShoppingCart.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if cart:
            cart.quantity = int(quantity)
            total = cart.calculate_total()
            db.session.commit()
            return jsonify({'message': 'Cart quantity updated successfully', 'total': total})
        else:
            abort(400, {'error': 'Product not found in the cart'})
        

@app.route("/shopping-cart/<string:product_id>", methods=['DELETE'])
@login_required
def delete_from_cart(product_id):
    """This a route that deletes items from cart"""
    if current_user.is_authenticated:
        cart = ShoppingCart.query.filter_by(
            user_id=current_user.id, product_id=product_id).first()
        
        if cart:
            db.session.delete(cart)
            db.session.commit()
            
            count_cart = ShoppingCart.query.filter_by(user_id=current_user.id).count()
            return jsonify({'message': 'Item deleted from the cart!', 'count_cart': count_cart}), 200
        else:
            return jsonify({'error': 'Item not found in the cart!'}), 404
        

@app.route("/order", methods=['GET', 'POST'])
@login_required
def order():
    return render_template("order_products.html", title='Order')

@app.context_processor
def global_variables():
    if current_user.is_authenticated:
        cart = ShoppingCart.query.filter_by(user_id=current_user.id).all()
        count_cart = len(cart)
    else:
        count_cart = 0
        
    return dict(count_cart=count_cart)
