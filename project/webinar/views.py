from flask import render_template, Blueprint, url_for, \
    redirect, flash, request

from project.models import Category, Webinar

webinar_blueprint = Blueprint('webinar', __name__,)
