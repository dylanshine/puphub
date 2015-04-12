import datetime

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_required, current_user

from project import db
from project.models import User, Category, Webinar
from .forms import WebinarCreateForm, WebinarEditForm

webinar_blueprint = Blueprint('webinar', __name__,)
