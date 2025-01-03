import click
from src.commands.add import add
from src.commands.create import create
from src.commands.checkout import checkout
from src.commands.commit import commit
from src.commands.stack import stack
from src.commands.push import push
from src.commands.auth import auth


@click.group()
@click.option("-v", "--verbose", "verbose", help="Use verbose logging", is_flag=True)
@click.pass_context
def cli(
    ctx: click.Context, verbose: bool = False,
):
    ctx.ensure_object(dict)
    
    ctx.obj["cli_args"] = ctx.params
    ctx.help_option_names = ["-h", "--help"]

# Add commands
cli.add_command(add)
cli.add_command(auth)
cli.add_command(create)
cli.add_command(checkout)
cli.add_command(commit)
cli.add_command(stack)
cli.add_command(push)

def main():
    """Entry point for the application"""
    cli(obj={})

if __name__ == "__main__":
    main()