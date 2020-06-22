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

The basic app structure includes a User model, public as well as secured API routes with endpoints to retrieve information about users, minimal error handling, an index page as well as some database configuration and unit testing setup. The template uses PostgreSQL databases for development and production and SQLite for testing.

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
(serve from one and access from another terminal window)
```shell
$ poetry run flask run
Serving Flask app...
```
```shell
$ curl http://127.0.0.1:5000/ping
Server is here
```

3. Add `API_KEY` to `.env` and test access to protected resource (make sure environment variables are loaded from file and restart Flask server)
```shell
$ curl --header "API_KEY: ..." http://127.0.0.1:5000/protected
Valid key provided
```

4. Create and serve development database and add specifications `.env`
```
DEV_DB_USER=
DEV_DB_PW=
DEV_DB_URL=
DEV_DB_NAME=
```

5. Initialize database
```shell
$ poetry run python manage.py db init
```

6. Update `migrations/env.py` with database specifications

 Replace
 ```python
 config.set_main_option(
     'sqlalchemy.url',
     str(current_app.extensions['migrate'].db.engine.url).replace('%', '%%'))
 ```
 with
 ```python
 config.set_main_option(
     'sqlalchemy.url',
     current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
 ```

7. Migrate and upgrade development database
```shell
$ export FLASK_ENV=development
$ poetry run python manage.py db migrate
$ poetry run python manage.py db upgrade
```

8. Test app locally with database
```shell
$ poetry run flask run
```
```shell
$ curl --header "API_KEY: ..." http://127.0.0.1:5000/v1/users
0 entries in DB
```

9. Run tests and determine coverage
```shell
$ poetry run coverage run -m unittest
[...]
Ran 10 tests
$ poetry run coverage report
[...]
TOTAL 157 0 100%
```

----

**Production environment**

10. Create and serve production database and add specifications `.env`
```
PROD_DB_USER=
PROD_DB_PW=
PROD_DB_URL=
PROD_DB_NAME=
```

11. Upgrade production database
```shell
$ export FLASK_ENV=production
$ poetry run python manage.py db upgrade
```

12. Create AWS S3 deployment bucket and add specifications including AWS environment variables to `zappa_settings.json`
(see more information about Zappa at https://github.com/Miserlou/Zappa)
```json
{
    "prod": {
        "app_function": "run.app",
        "runtime": "python3.8",
        "aws_region": ,
        "profile_name": ,
        "s3_bucket": ,
        "keep_warm": false,
        "aws_environment_variables": {
            "API_KEY": ,
            "PROD_DB_USER": ,
            "PROD_DB_PW": ,
            "PROD_DB_URL": ,
            "PROD_DB_NAME": ,
        },
    }
}
```


13. Deploy app and test in production
```shell
$ poetry run zappa deploy
```

## Contribution

Please submit any [issues](https://github.com/kinosal/flask-template/issues) you have. If you have any ideas how to further improve the template please get in touch or feel free to fork this project and create a pull request with your proposed updates.
