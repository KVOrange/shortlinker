from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from app.handlers.json_handler import get_response

module = Blueprint('user_req', __name__, url_prefix='/user')
#
#
# @module.route('/link', methods=['GET'])
# @jwt_required()
# def get_links():
#     links_info = [
#         {
#             'serv_name': link.name,
#             'url': link.url,
#             'description': link.description,
#             'type': link.type,
#             'click_count': link.click_count,
#         } for link in current_user.links]
#     return get_response(200, True, '', info=links_info)
