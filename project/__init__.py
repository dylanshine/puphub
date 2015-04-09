from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from project.default.views import default_blueprint

app.register_blueprint(default_blueprint)
