from typing import Optional

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
from pydantic import BaseModel, HttpUrl, validator

from app.enums.link_types import LinkTypes
from app.handlers.json_handler import get_response
from app.models import Link
from app.models import db
from app.modules.link_hash import hash_generator

module = Blueprint('link', __name__, url_prefix='/')


class LinkDefaultCreateData(BaseModel):
    url: HttpUrl


class LinkAuthCreateData(BaseModel):
    url: HttpUrl
    name: Optional[str] = None
    type: Optional[int] = 0
    description: Optional[str] = None

    @validator('name', always=True)
    def check_name(cls, name):
        if name:
            if len(name) > 30:
                raise ValueError('Слишком большое название ссылки.')
            link = Link.query.filter_by(name=name).first()
            if link:
                raise ValueError('Имя для ссылки уже занято.')
        return name

    @validator('type', always=True)
    def check_type(cls, type):
        if type not in LinkTypes.all_link_types():
            raise ValueError('Указан неккоректный тип ссылки.')
        return type


@module.route('/<string:link_name>', methods=['GET'])
def link(link_name):
    user_link = Link.query.filter_by(name=link_name).first()
    if not user_link:
        return get_response(False, 400, 'Ссылка не найдена')  # TODO: редирект на 404 для ссылки
    if user_link.type != LinkTypes.PUBLIC.value:
        if current_user.is_anonymous:
            return get_response(False, 400, 'Ссылка не найдена')  # TODO: редирект на авторизацию
        if user_link.type == LinkTypes.PERSONAL and user_link.user != current_user:
            return get_response(False, 403, 'Ссылка защищена владельцем. Переход невозможен!')
    user_link.add_new_click()
    return redirect(user_link.url, code=302)


@module.route('/link/default_create', methods=['POST'])
def link_default_create():
    try:
        req_data = LinkDefaultCreateData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Неккоректный URL', data=error.errors())
    new_link = Link()
    new_link.url = req_data.url
    new_link.name = hash_generator()
    db.session.add(new_link)
    db.session.commit()
    return get_response(200, True, '', link=request.url_root + new_link.name)


@module.route('/link/auth_create', methods=['POST'])
@login_required
def link_auth_create():
    try:
        req_data = LinkAuthCreateData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Неккоректный запрос', data=error.errors())
    new_link = Link()
    new_link.url = req_data.url
    if not req_data.name:
        new_link.name = hash_generator()
    else:
        new_link.name = req_data.name
    new_link.description = req_data.description
    new_link.type = req_data.type
    db.session.add(new_link)
    current_user.links.append(new_link)
    db.session.commit()
    return get_response(200, True, '', link=request.url_root + new_link.name)
