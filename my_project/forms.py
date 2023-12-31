from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from my_project.models import User


class SignupForm(FlaskForm):
    """This is a sign up form"""
    fullname = StringField('Full Name', validators=
                           [DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=
                        [DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=
                             [DataRequired(), Length(min=6, max=15)])
    confirm_password = PasswordField('Confirm Password', validators=
                                     [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        """To check if email is valid"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already exist')
        
    def validate_phone_number(self, phone_number):
        """To check if the phone number is valid"""
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('phone number already exist')


class LoginForm(FlaskForm):
    """This is a login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UploadProductForm(FlaskForm):
    """This is a form for uploading products"""
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_desc = TextAreaField('Product Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    category = SelectField('Category', coerce=str, validators=[DataRequired()])
    product_image = FileField('Product Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload Product')


class ReviewForm(FlaskForm):
    """This is a form for product reviews"""
    review_text = TextAreaField('Review Text', validators=[DataRequired(), Length(min=1, max=500)])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    fullname = StringField('Full Name', validators=
                           [DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ShoppingCartForm(FlaskForm):
    """This is a form for shopping cart"""
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])