from flask import render_template, Blueprint

default_blueprint = Blueprint(
    'default', __name__, url_prefix='', template_folder='templates', static_folder='static')


@default_blueprint.route('/about')
def about():
    return render_template('about.html')


@default_blueprint.route('/')
def index():
    return render_template('index.html')
