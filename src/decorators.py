

from functools import wraps

import click
from src.util import get_token


def auth_required(f):
    """Decorator to check for authentication before running commands"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        token = get_token()
        if not token:
            raise click.ClickException(
                "Authentication required. Please run 'gx auth --token <YOUR_TOKEN>' first"
            )
        return f(*args, **kwargs)
    return wrapped