from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from opentok import OpenTok

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)
opentok_sdk = OpenTok(
    app.config['OT_API_KEY'], app.config['OT_API_SECRET'])


from project.main.views import main_blueprint
from project.user.views import user_blueprint
from project.category.views import category_blueprint
from project.webinar.views import webinar_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(webinar_blueprint)


from project.models import User, Category, Webinar

login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"
