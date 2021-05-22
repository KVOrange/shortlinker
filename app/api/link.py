from datetime import datetime
from typing import Optional

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
from pydantic import BaseModel, HttpUrl, validator

from app.enums.link_types import LinkTypes
from app.handlers.json_handler import get_response
from app.models import Link, LinkStatistic
from app.models import db
from app.modules.link_hash import hash_generator

module = Blueprint('link', __name__, url_prefix='/l')


class LinkDefaultCreateData(BaseModel):
    url: HttpUrl


class LinkStatisticData(BaseModel):
    name: str
    datetime_start: datetime
    datetime_end: datetime


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


class LinkUpdateData(BaseModel):  # TODO: продумать наследование
    name: str
    new_name: Optional[str] = None
    type: Optional[int] = 0
    description: Optional[str] = None

    @validator('new_name', always=True)
    def check_name(cls, new_name):
        if new_name:
            if len(new_name) > 30:
                raise ValueError('Слишком большое название ссылки.')
            link = Link.query.filter_by(name=new_name).first()
            if link:
                raise ValueError('Имя для ссылки уже занято.')
        return new_name

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


@module.route('/link/statistic', methods=['POST'])
@login_required
def link_statistic():
    try:
        req_data = LinkStatisticData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Неккоректный запрос', data=error.errors())
    user_link = Link.query.filter_by(name=req_data.name, user=current_user).first()
    if not user_link:
        return get_response(400, False, 'Ссылка не найдена')
    statistics = db.session.query(LinkStatistic).filter(
        LinkStatistic.link_id == user_link.id,
        LinkStatistic.date.between(req_data.datetime_start, req_data.datetime_end)
    )
    info = [{'date': stat.date.strftime("%d.%m.%Y %H:%M:%S")} for stat in statistics]
    return get_response(200, False, '', info = info)


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
    return get_response(200, True, '', link=request.url_root + 'l/' + new_link.name)


@module.route('/link/update', methods=['PUT'])
@login_required
def link_update():
    try:
        req_data = LinkUpdateData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Неккоректный запрос', data=error.errors())
    user_link = Link.query.filter_by(name=req_data.name).first()
    if not user_link:
        return get_response(400, False, 'Ссылка не найдена')
    if user_link.user != current_user:
        return get_response(403, False, 'Отказано в доступе')
    if req_data.new_name:
        user_link.name = req_data.new_name
    if req_data.type:
        user_link.type = req_data.type
    if req_data.description:
        user_link.description = req_data.description
    db.session.commit()
    return get_response(200, True, '', link=request.url_root + 'l/' + user_link.name)
