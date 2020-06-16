# flask-template

A simple template to initialize a Python web app with a RESTful API based on the [Flask framework](https://github.com/pallets/flask)

## Structure

```bash
├── app
│   ├── api
│   │   └── ...
│   ├── models
│   │   └── ...
│   ├── templates
│   │   └── ...
│   ├── __init__.py
│   ├── config.py
├── tests
│   └── ...
├── manage.py
├── run.py
└── ...
```

The basic app structure includes a User model, API routes with endpoints to retrieve information about users, minimal error handling, a simple index page as well as some database configuration and unit testing setup. The template uses PostgreSQL databases for development and production and SQLite for testing.

## Environment

- Python 3.8
- Poetry (package manager)
- Flask (web framework)
- SQLAlchemy (ORM)
- Psycopg (PostgreSQL adapter)
- Zappa (deployment to AWS Lambda)

## Setup

1. Create virtual environment and install dependencies
(see more information about Poetry at https://github.com/python-poetry/poetry)
```shell
$ poetry install
```

2. Test app locally without database
```shell
$ poetry run flask run
```
 --> http://127.0.0.1:5000

3. Create database and add specifications to **.env**

4. Initialize database
```shell
$ poetry run python manage.py db init
```

5. Update **migrations/env.py** with database specifications
```python
from flask import current_app
config.set_main_option(
    'sqlalchemy.url', current_app.config.get(
        'SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata
```

6. Migrate and upgrade database in appropriate environments
```shell
$ poetry run python manage.py db migrate
$ export FLASK_ENV=development
$ poetry run python manage.py db upgrade
$ export FLASK_ENV=production
$ poetry run python manage.py db upgrade
```

7. Test app locally with database
```shell
$ poetry run flask run
```
 --> http://127.0.0.1:5000/users

8. Run tests
```shell
$ poetry run python tests/tests.py
```

9. Determine test coverage
```shell
$ poetry run coverage run -m unittest
$ poetry run coverage report
```

10. Create AWS S3 deployment bucket and add specifications to **zappa_settings.json**
(see more information about Zappa at https://github.com/Miserlou/Zappa)

11. Deploy app and test in production
```shell
$ poetry run zappa deploy
```

## Contribution

Please submit any [issues](https://github.com/kinosal/flask-template/issues) you have. If you have any ideas how to further improve the template please get in touch or feel free to fork this project and create a pull request with your proposed updates.
