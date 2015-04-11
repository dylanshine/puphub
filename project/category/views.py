from flask import render_template, Blueprint, url_for, \
    redirect, flash, request

from project.models import Category, Webinar
from .helpers import slugify

category_blueprint = Blueprint('category', __name__,)
