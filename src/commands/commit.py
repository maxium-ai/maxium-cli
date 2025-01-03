import click

from src.util import get_line_changes, run_git_command
from src.config import config


@click.command()
@click.option('-m', '--message', required=True, help='Commit message')
@click.option('--force', is_flag=True, help='Force commit without stacking prompt')
def commit(message: str, force: bool) -> None:
    """Commit staged changes"""
    current_branch = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    try:
        threshold = int(run_git_command(['git', 'config', f'branch.{current_branch}.stackThreshold']))
    except:
        threshold = config.STACKING_THRESHOLD
    
    lines_changed = get_line_changes()
    
    # Proceed with commit
    run_git_command(['git', 'commit', '-m', message])
    
    # TODO: run this prior to git push instead
    if lines_changed > threshold and not force:
        click.echo("\n✨ Change is potentially large enough for stacking (commit with --force to ignore)")
        click.echo("Run 'gx stack' to split this change into smaller commits (if eligible)")