
from flask import render_template, Blueprint
module = Blueprint('view', __name__, url_prefix='/',  template_folder="jinja_templates")

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
    temp = [1,2,3,4,5]
    return render_template('cabinet.html', link_info_list=temp)