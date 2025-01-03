import click
import subprocess
import os
import json
from pathlib import Path
from src.config import config

def run_git_command(command, check=True):
    """Run a git command and return its output"""
    try:
        result = subprocess.run(
            command, check=check, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e.stderr}", err=True)
        if check:
            raise click.Abort()
        return e.stderr

def get_commit_diff(commit_hash: str, parent_hash: str) -> str:
   """Get the diff between a commit and its parent"""
   return run_git_command(['git', 'diff', parent_hash, commit_hash])

def get_config_path():
    """Get the path to the config file"""
    home = Path.home()
    return home / f'.{config.CLI_CONFIG_EXTENSION}'

def save_token(token: str) -> None:
    """Save token to config file"""
    config_path = get_config_path()
    config = {'token': token}
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f)
        os.chmod(config_path)
    except Exception as e:
        raise click.ClickException(f"Failed to save token: {str(e)}")

def get_token() -> str | None:
    """Get token from config file"""
    config_path = get_config_path()
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('token')
    except FileNotFoundError:
        return None
    except Exception as e:
        raise click.ClickException(f"Failed to read token: {str(e)}")


def get_line_changes():
    """Get number of lines changed in staged files"""
    try:
        diff_stats = run_git_command(['git', 'diff', '--cached', '--numstat'])
        total_additions = 0
        total_deletions = 0
        
        if diff_stats:
            for line in diff_stats.splitlines():
                if line.strip():
                    additions, deletions, _ = line.split('\t')
                    if additions != '-':
                        total_additions += int(additions)
                    if deletions != '-':
                        total_deletions += int(deletions)
                        
        return total_additions + total_deletions
    except:
        return 0
    

def remote_branch_exists(branch_name: str) -> bool:
    """Check if branch exists on remote"""
    output = run_git_command(['git', 'ls-remote', '--heads', 'origin', branch_name])
    return bool(output.strip()) 
