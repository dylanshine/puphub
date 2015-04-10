import datetime

from project import app, db
from project import models
from project.models import User
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="ad@min.com",
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    )
    db.session.commit()

if __name__ == '__main__':
    manager.run()
