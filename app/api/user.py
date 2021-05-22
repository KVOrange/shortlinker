from flask import Blueprint, request, render_template
from flask_login import login_user, login_required, current_user
from pydantic import BaseModel
from pydantic.networks import EmailStr
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Link
from app.handlers.json_handler import get_response
from app.models import User, db

module = Blueprint('user_req', __name__, url_prefix='/user')

@module.route('/link', methods=['GET'])
@login_required
def get_links():
    links_info = [
        {
            'serv_link': request.url_root + 'l/' + link.name,
            'url': link.url,
            'description': link.description,
            'type': link.type,
            'click_count': link.click_count,
        }for link in current_user.links]
    return get_response(200, True, '', info=links_info)