from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return "Hello, We're GPTPRO!"


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))
