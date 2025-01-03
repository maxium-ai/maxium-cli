import click

from src.util import run_git_command


@click.command()
@click.argument('branch_name')
def checkout(branch_name: str) -> None:
    """Checkout a branch"""
    run_git_command(['git', 'checkout', branch_name])
    click.echo(f"Switched to branch: {branch_name}")