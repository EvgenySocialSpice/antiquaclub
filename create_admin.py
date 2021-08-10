from getpass import getpass
import sys
from auctionapp.db import db
from auctionapp import create_app
from auctionapp.user.models import User, db

app = create_app()

with app.app_context():
    email = input('Введите ваш имейл:')

    if User.query.filter(User.email == email).count():
        print('Пользователь с таким именем уже существует')
        sys.exit(0)

    password1 = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2:
        print('Пароли не одинаковые')
        sys.exit(0)

    new_user = User(email=email, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
