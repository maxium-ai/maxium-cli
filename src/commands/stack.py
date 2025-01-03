import click
from src.decorators import auth_required
from src.services.auto_stacking import auto_stack_commits
from src.util import get_commit_diff, run_git_command


@click.command()
# @auth_required
def stack() -> None:
    """Analyse and stack recent commits based on their changes"""
    status = run_git_command(['git', 'status', '--porcelain'])
    if status:
        raise click.UsageError("Working directory is not clean. Please commit you changes before stacking.")
    
    current_branch = run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

    try:
        base_branch = click.prompt("Please specify the base branch (e.g., main, master)", type=str)
            
        try:
            run_git_command(['git', 'rev-parse', '--verify', base_branch])
        except:
            raise click.ClickException(f"Base branch '{base_branch}' does not exist")
            
        current_commits = run_git_command(['git', 'log', '--pretty=format:"%H|%P|%s"', f'{base_branch}..{current_branch}'])
        current_commits = [commit.strip('"').split('|') for commit in current_commits.splitlines()]
    except:
        raise click.ClickException(f"Could not find commits in history")

    if len(current_commits) == 0:
        raise click.ClickException("No commits found to stack. Commit your changes first.")
    elif len(current_commits) == 1:
        raise click.ClickException("Single commit changes are not supported for auto-stacking yet.")

    click.echo("📊 Analysing commits...")
    stacking_request_data = []   
    order = len(current_commits)
    for commit in current_commits:
        commit_hash, parent_hash, commit_msg = commit
        diff = get_commit_diff(commit_hash, parent_hash.split()[0])
        
        stacking_request_data.append({
            'hash': commit_hash, 'message': commit_msg, 'diff': diff, 'parent': parent_hash, 'order': order
        })
        order -= 1

    click.echo("🔍 Determining optimal stacking strategy...")
    try:
        stacking_response = auto_stack_commits(stacking_request_data)
        
        if not stacking_response.get('needs_stacking'):
            click.echo(f"\n✨ Good news! {stacking_response['reason']}")
            return
            
        stacks = sorted(stacking_response['stacks'], key=lambda x: x['order'])
        
        click.echo("\n📋 Proposed stacking strategy:")

        first_stack = stacks[0]
        click.echo(f"\n▶ Current Branch: {current_branch}")
        click.echo(f"  Description: {first_stack['description']}")
        click.echo("  Commits:")
        for commit in first_stack['commits']:
            click.echo(f"    - {commit['message']}")
            
        commits = []
        commits.extend(first_stack['commits'])
        
        for i, stack in enumerate(stacks[1:], 1):
            click.echo(f"\n▶ Stack#{i}: {current_branch}-stack-{i}")
            click.echo(f"  Description: {stack['description']}")
            click.echo("  Commits:")
            
            commits.extend(stack['commits'])
            
            for commit in commits:
                click.echo(f"    - {commit['message']}")
                
        if not click.confirm("\nWould you like to create these stacks?"):
            click.echo("Stacking cancelled")
            return
            
    except click.ClickException as e:
        click.echo(f"Error: {str(e)}")
        return

    click.echo("\n📦 Creating stacked branches...")
    created_branches = []
    
    previous_branch_name = current_branch
    n_stacked_commits = 0
    for stack in reversed(stacks):
        new_branch_name = f"{current_branch}-stack-{stack['order']-1}"
        try:
            run_git_command(['git', 'checkout', '-b', new_branch_name, previous_branch_name])
            
            if n_stacked_commits > 0:
                run_git_command(['git', 'reset', '--hard', f'HEAD~{str(n_stacked_commits)}'])

            previous_branch_name = new_branch_name
            n_stacked_commits = len(stack['commits'])

            created_branches.append({
               'branch': new_branch_name, 'commits': stack['commits'], 'description': stack['description']
           })

        except Exception as e:
            click.echo(f"Error creating stack {new_branch_name}: {str(e)}")

            run_git_command(['git', 'checkout', current_branch])
            run_git_command(['git', 'branch', '-d', new_branch_name], check=False)

            raise click.ClickException(f"Failed to create stacks: {str(e)}")
                
    run_git_command(['git', 'branch', '-f', current_branch, previous_branch_name])
    run_git_command(['git', 'checkout', current_branch])

    if created_branches:
        click.echo("\n🎋 Successfully created stacks:")
        click.echo(f"\n▶ {current_branch}")
        click.echo(f"  Description: {first_stack['description']}")
        click.echo("  Commits:")
        for commit in first_stack['commits']:
            click.echo(f"    - {commit['message']}")
        
        for stack in created_branches:
            click.echo(f"\n▶ {stack['branch']}")
            click.echo(f"  Description: {stack['description']}")
            click.echo("  Commits:")
            for commit in stack['commits']:
                click.echo(f"    - {commit['message']}")
        
        click.echo("\n💡 Next steps:")
        click.echo("1. Review the created stacks")
        click.echo("2. Switch to each branch:")
        for stack in created_branches:
            click.echo(f"   `gx checkout` {stack['branch']}")
        click.echo("3. Push your changes:")
        click.echo("   `gx push`")
        click.echo("4. Optional: Revert stacking on current branch by using `git branch`")
