import click

from src.util import remote_branch_exists, run_git_command


@click.command()
def push() -> None:
    """Push changes to remote"""
    current_branch = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    
    if remote_branch_exists(current_branch):
        try:
            run_git_command(['git', 'push'])
        except click.Abort:
            click.echo("Failed to push changes. Please ensure you have access to the remote repository.", err=True)
            return
    else:
        try:
            run_git_command(['git', 'push', '--set-upstream', 'origin', current_branch])
        except click.Abort:
            click.echo("Failed to push changes. Please ensure you have access to the remote repository.", err=True)
            return

    click.echo(f"Successfully pushed changes to {current_branch}")