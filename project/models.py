import datetime
from slugify import slugify

from project import db, bcrypt

student_table = db.Table(
    'student',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('webinar_id', db.Integer, db.ForeignKey('webinar.id'))
)


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    webinars = db.relationship("Webinar", backref="user")

    def __init__(self, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None, rating=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.rating = rating

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)


class Category(db.Model):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    webinars = db.relationship("Webinar", backref="category")

    def __init__(self, title):
        self.title = title
        self.slug = slugify(title)

    def __repr__(self):
        return '<Category: {}'.format(self.title)


class Webinar(db.Model):

    __tablename__ = "webinar"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    finish = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    students = db.relationship(
        'User', secondary=student_table, backref=db.backref('webinar', lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Webinar: {}'.format(self.title)
