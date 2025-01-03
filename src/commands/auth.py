import click

from src.util import save_token


@click.command()
@click.option('--token', required=True, help='User authentication token retrieved from account admin')
def auth(token: str) -> None:
    """Authenticate user for use of Maxium CLI"""
    try:
        save_token(token)
        # TODO: validate token with server?
        click.echo("Authenticated successfully!")
    except Exception as e:
        raise click.ClickException(f"Authentication failed: {str(e)}")