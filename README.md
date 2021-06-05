# Web Analyzer (Scalable Scraper) MVP

Flask RESTful API: https://l3p7kh8vc3.execute-api.eu-west-1.amazonaws.com/prod/v1/

## Structure

```bash
├── app
│   ├── api
│   │   └── ...
│   ├── models
│   │   └── ...
│   ├── scripts
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

## Environment

- Python 3.8
- Poetry (package manager)
- Flask (web framework)
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

4. Run tests and determine coverage
```shell
$ poetry run coverage run -m unittest
[...]
$ poetry run coverage report
[...]
```

----

**Production environment**

5. Create AWS S3 deployment bucket and add specifications including AWS environment variables to `zappa_settings.json`
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
        },
    }
}
```


6. Deploy app and test in production
```shell
$ poetry run zappa deploy
```
