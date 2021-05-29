
from flask import json, render_template, Blueprint, request, redirect
import requests
from werkzeug.wrappers import AcceptMixin
from app import front_app
module = Blueprint('view', __name__, url_prefix='/',
                   template_folder="jinja_templates")


@module.route('/')
def index():
    return render_template('mainpage.html')


@module.route('/authtorization')
def auth():
    return render_template('authtorization.html')


@module.route('/notfound')
def notfound():
    return render_template('notfound.html')


@module.route('/lk')
def lk():
    resp = front_app.test_client().get(
        '{0}api/user/link'.format(request.url_root),
         headers={
             'Content-Type': 'application/json',
             'Accept': 'application/json',
             'Authorization': request.cookies.get('JWT')
    })
    temp = json.loads(resp.data).get('info')
    if temp:
        return render_template('cabinet.html', link_info_list=temp, server_root=request.url_root)
    else:
        return render_template('cabinet.html')

@module.route('/l/<string:link_name>')
def link_redirect(link_name):
    new_link = front_app.test_client().get(
        '{0}api/link/{1}'.format(request.url_root,link_name),
         headers={
             'Content-Type': 'application/json',
             'Accept': 'application/json',
             'Authorization': request.cookies.get('JWT')
    })
    
    req_data = json.loads(new_link.data)
    print(req_data)
    if req_data.get('success'):
        return redirect(req_data.get('url'))
