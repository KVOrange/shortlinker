from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from pydantic import BaseModel
from pydantic.networks import EmailStr
from werkzeug.security import generate_password_hash, check_password_hash

from app.handlers.json_handler import get_response
from app.models import User, db

module = Blueprint('auth', __name__, url_prefix='/api/auth')


class RegData(BaseModel):
    """Класс валидатор входных данных для запроса регистрации"""
    login: str
    password: str
    name: str
    surname: str
    email: EmailStr


class LoginData(BaseModel):
    """Класс валидатор входных данных для запроса авторизации"""
    login: str
    password: str


@module.route('/login', methods=['POST'])
def login():
    """Запрос авторизации пользователя в системе.

    :return: Ответ сервера, содержащий JWT токен пользователя при успешном запросе.
    """
    try:
        req_data = LoginData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
    user = User.query.filter_by(login=req_data.login).first()
    if not user or not check_password_hash(user.password, req_data.password):
        return get_response(400, False, 'Неверный логин и/или пароль!')
    return get_response(200, True, '', token=user.get_token())


@module.route('/registration', methods=['POST'])
def registration():
    """Запрос регистрации новых пользователей в системе.

    :return: Ответ сервера, содержащий JWT токен нового пользователя при успешном запросе.
    """
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
    return get_response(200, False, '', token=new_user.get_token())
