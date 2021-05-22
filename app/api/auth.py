from flask import Blueprint, request, render_template
from flask_login import login_user, login_required
from pydantic import BaseModel
from pydantic.networks import EmailStr
from werkzeug.security import generate_password_hash, check_password_hash

from app.handlers.json_handler import get_response
from app.models import User, db

module = Blueprint('auth', __name__, url_prefix='/auth')


class RegData(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    email: EmailStr


class LoginData(BaseModel):
    login: str
    password: str


@module.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


@module.route('/testlog', methods=['GET'])
@login_required
def testlog():
    return render_template('testlogin.html')


@module.route('/login', methods=['POST'])
def login():
    user_login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=user_login).first()
    if not user or not check_password_hash(user.password, password):
        return get_response(400, False, 'Неверный логин и/или пароль!')
    login_user(user, remember=True)
    return render_template('test.html')


@module.route('/registration', methods=['POST'])
def registration():
    try:
        req_data = RegData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
    if User.query.filter_by(login=req_data.login).first():
        return get_response(400, False, 'Пользователь с таким логином уже существует')
    if User.query.filter_by(email=req_data.email).first():
        return get_response(400, False, 'Пользователь с такой почтой уже существует')
    new_user = User()
    new_user.login = req_data.login
    new_user.password = generate_password_hash(req_data.password, method='sha256')
    new_user.email = req_data.email
    new_user.name = req_data.name
    new_user.surname = req_data.surname
    db.session.add(new_user)
    db.session.commit()
    return get_response(400, False, '', user_id=new_user.id)
