"""Database migration and upgrade manager."""

from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from app import config
from app import create_app
from app import db

app = create_app(config.set_config())
app.app_context().push()

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
