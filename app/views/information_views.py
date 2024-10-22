from flask import Blueprint, render_template

bp = Blueprint('information_views', __name__, url_prefix='/information')

@bp.route('/')
def information():
    return render_template('front/info.html')
