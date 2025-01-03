from typing import Any
import click
from src.util import run_git_command
from src.config import config

def validate_threshold(ctx: click.Context, param: click.Parameter | None, value: Any) -> int:
    if value <= 0:
        raise click.BadParameter("Threshold must be greater than 0")
    return value

@click.command()
@click.argument('branch_name')
@click.option(
    '--threshold', 
    default=config.STACKING_THRESHOLD, 
    type=int, 
    callback=validate_threshold, 
    help='Line changes threshold for stacking suggestion'
)
def create(branch_name: str, threshold: int) -> None:
    """Create a new feature branch"""
    run_git_command(['git', 'checkout', '-b', branch_name])
    run_git_command([
        'git', 'config', f'branch.{branch_name}.stackThreshold', str(threshold)
    ])
    
    click.echo(f"Created and switched to new branch: {branch_name}")
    click.echo(f"Stack threshold set to {str(threshold)} lines. Changes larger than this will suggest stacking.")
    
    try:
        run_git_command(['git', 'push', '--set-upstream', 'origin', branch_name])
    except click.Abort:
        click.echo("Branch created locally only - will be pushed on first 'gx push'")
