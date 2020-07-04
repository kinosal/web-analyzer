"""Lambda handler functions to execute scheduled jobs remotely,
see https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html

Specify in zappa_settings.json:

"events": [
    {
        "function": "app.scripts.handler.script_handler",
        "kwargs": {"key": "value"},
        "expression": "cron(00 00 * * ? *)"
    },
],

"""

from app.scripts.script import script_function


def script_handler(event: object, context: object = None) -> None:  # pragma: no cover
    """Calls script_function from Lambda
    Args:
        event: Lambda event
        context: Lambda context (unused)
    """
    # Retrieve required kwarg(s) from Lambda event
    arg = event['kwargs']['key']

    # Call desired function(s)
    script_function(arg)
