from flask import render_template, Blueprint, url_for, \
    redirect, flash, request

from project.models import Category, Webinar

category_blueprint = Blueprint('category', __name__,)


@category_blueprint.route('/categories')
def index():
    categories = Category.query.all()
    return render_template('category/index.html', categories=categories)


@category_blueprint.route('/category/<category_slug>')
def show(category_slug):
    category = Category.query.filter_by(slug=category_slug).first()
    return render_template('category/show.html', category=category)
