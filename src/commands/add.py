import subprocess

import click

from src.util import run_git_command


@click.command()
@click.argument('files', nargs=-1)
def add(files):
    """Add files to git staging"""
    if not files:
        click.echo("Error: Please specify files to add", err=True)
        return
    
    try:
        before_status = run_git_command(['git', 'status', '--porcelain'])
        
        for file in files:
            run_git_command(['git', 'add', file])
        
        after_status = run_git_command(['git', 'status', '--porcelain'])
        new_changes = len(after_status.splitlines()) - len(before_status.splitlines())
        
        if '.' in files:
            # If adding all files, show a summary
            click.echo("Added all changes to staging:")
            status = run_git_command(['git', 'status', '-s'])
            click.echo(status)
        else:
            click.echo(f"Added {len(files)} file(s) to branch")
            
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e.stderr}", err=True)
        raise click.Abort()