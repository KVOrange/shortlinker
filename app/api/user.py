from typing import Optional

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from pydantic import BaseModel, EmailStr, constr
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from app.handlers.json_handler import get_response

module = Blueprint('user_req', __name__, url_prefix='/api/user')


class UserUpdateData(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None


class ChangePasswordData(BaseModel):
    old_password: str
    new_password: constr(min_length=8)


@module.route('/', methods=['GET', 'PUT'])
@jwt_required()
def user_req():
    if request.method == 'GET':
        resp_data = {
            'login': current_user.login,
            'email': current_user.email,
            'name': current_user.name,
            'surname': current_user.surname,
        }
        return get_response(200, True, '', info=resp_data)

    if request.method == 'PUT':
        try:
            req_data = UserUpdateData.parse_raw(request.data)
        except ValueError as error:
            return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
        if req_data.name:
            current_user.name = req_data.name
        if req_data.surname:
            current_user.surname = req_data.surname
        if req_data.email:
            current_user.email = req_data.email
        db.session.commit()
        return get_response(200, True, '')


@module.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        req_data = ChangePasswordData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
    if not check_password_hash(current_user.password, req_data.old_password):
        return get_response(403, False, 'Старый пароль неверен')
    current_user.password = generate_password_hash(req_data.new_password)
    db.session.commit()
    return get_response(200, True, '')


@module.route('/link', methods=['GET'])
@jwt_required()
def get_links():
    links_info = [
        {
            'serv_name': short_link.name,
            'url': short_link.full_link.url,
            'description': short_link.description,
            'type': short_link.type,
            'click_count': short_link.click_count,
        } for short_link in current_user.short_links]
    return get_response(200, True, '', info=links_info)
