from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField, SubmitField, StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from auctionapp.user.models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('отправить')


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    last_name = StringField('Фамилия пользователя', validators=[DataRequired()])
    nickname = StringField('Псевдоним', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired()])
    birth_date = DateField('Дата рождения', format="%d/%m/%Y", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Отправить!')

    def validate_nick_name(self, nickname):
        user_count = User.query.filter_by(nickname=nickname.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует!')

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким почтовым адресом уже существует!')

    def validate_phone(self, phone):
        user_count = User.query.filter_by(phone=phone.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким телефоном уже существует!')
    
    # def validate_birth_date(self, birth_date):
        
    
        
    

