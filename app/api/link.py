"""Модуль запросов, связанных с ссылками."""

from datetime import datetime
from typing import Optional

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from pydantic import BaseModel, HttpUrl, validator

from app.database import db
from app.enums.link_types import LinkTypes
from app.handlers.json_handler import get_response
from app.models import FullLink, ShortLink

module = Blueprint('link', __name__, url_prefix='/api/link')


class LinkUpdateData(BaseModel):
    """Класс валидатор для данных запроса обновления информации о ссылке"""
    name: Optional[str] = None
    type: Optional[int] = 0
    description: Optional[str] = None

    @validator('name', always=True)
    def check_name(cls, name):
        """Фунция проверки допустимости имени ссылки"""
        if name:
            if len(name) > 30:
                raise ValueError('Слишком большое название ссылки.')
            link = ShortLink.query.filter_by(name=name).first()
            if link:
                raise ValueError('Имя для ссылки уже занято.')
        return name

    @validator('type', always=True)
    def check_type(cls, type):
        """Функция проверки корректности типа ссылки"""
        if type not in LinkTypes.all_link_types():
            raise ValueError('Указан неккоректный тип ссылки.')
        return type


class LinkCreateData(LinkUpdateData):
    """Класс валидатор данных запроса создания ссылки"""
    url: HttpUrl


class LinkStatisticData(BaseModel):
    """Класс валидатор данных запроса выдачи статистики ссылки"""
    name: str
    datetime_start: datetime
    datetime_end: datetime


@module.route('/<string:link_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required(optional=True)
def link(link_name):
    """Функция обработки стандартных запросов связанных с ссылками.

    :param link_name: имя ссылки.
    :return: Ответ сервера.
    """
    if request.method == 'GET':
        short_link = ShortLink.query.filter_by(name=link_name).first()
        if not short_link:
            return get_response(400, False, 'Ссылка не найдена')
        if short_link.type == LinkTypes.ONLY_AUTH.value and not current_user:
            return get_response(403, False, 'Ссылка доступна только авторизованным пользователям')
        if short_link.type == LinkTypes.PERSONAL.value and current_user != short_link.user:
            return get_response(403, False, 'Ссылка недоступна')
        if short_link.user:
            short_link.add_new_click()
        return get_response(200, True, '', url=short_link.full_link.url)

    if request.method == 'POST':
        if link_name != 'add':
            return get_response(404, False, 'Запрос отсутствует')
        try:
            req_data = LinkCreateData.parse_raw(request.data)
        except ValueError as error:
            return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
        full_link = FullLink.get_or_create(req_data.url)
        if not current_user:
            short_link = ShortLink.get_or_create(None, full_link, LinkTypes.PUBLIC.value)
            return get_response(200, True, '', link_name=short_link.name)
        if ShortLink.query.filter_by(user=current_user, full_link=full_link).first():
            return get_response(400, False, 'У вас уже создана ссылка для данного сайта')
        short_link = ShortLink.get_or_create(
            current_user,
            full_link,
            req_data.type,
            name=req_data.name,
            description=req_data.description,
        )
        return get_response(200, True, '', link_name=short_link.name)

    if request.method == 'PUT':
        if not current_user:
            return get_response(401, False, 'UNAUTHORIZED')
        short_link = ShortLink.query.filter_by(name=link_name, user=current_user).first()
        if not short_link:
            return get_response(400, False, 'Ссылка не найдена')
        try:
            req_data = LinkUpdateData.parse_raw(request.data)
        except ValueError as error:
            return get_response(400, False, 'Проверьте правильность запроса', data=error.errors())
        if req_data.name:
            short_link.name = req_data.name
        if req_data.description:
            short_link.description = req_data.description
        if req_data.type:
            short_link.type = req_data.type
        db.session.commit()
        return get_response(200, True, '')

    if request.method == 'DELETE':
        if not current_user:
            return get_response(401, False, 'UNAUTHORIZED')
        short_link = ShortLink.query.filter_by(name=link_name, user=current_user).first()
        print(short_link)
        if not short_link:
            return get_response(400, False, 'Ссылка не найдена')
        db.session.delete(short_link)
        db.session.commit()
        return get_response(200, True, '')


@module.route('/info/statistic', methods=['POST'])
@jwt_required()
def link_statistic():
    """Функция выдачи статистики ссылки за определенный период времени.

    :return: Ответ сервера.
    """
    try:
        req_data = LinkStatisticData.parse_raw(request.data)
    except ValueError as error:
        return get_response(400, False, 'Неккоректный запрос', data=error.errors())
    short_link = ShortLink.query.filter_by(name=req_data.name, user=current_user).first()
    if not short_link:
        return get_response(400, False, 'Ссылка не найдена')
    info = short_link.get_statistic(req_data.datetime_start, req_data.datetime_end)
    return get_response(200, False, '', info=info)
