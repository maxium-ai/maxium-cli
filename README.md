# Maxium CLI

A Git-native CLI tool that simplifies Git workflows and helps manage feature branches more efficiently.

## Installation

Install directly from GitHub using SSH:

```bash
pip install git+ssh://git@github.com/maxium-ai/maxium-cli.git@latest
```

## Features

### Better branch management
- `gx create <branch-name>`: Create and set up new feature branches with automatic size limits
- `gx checkout <branch-name>`: Switch between branches with enhanced history management
- `gx add [files]`: Stage files with improved feedback

### Auto-stacking of large PRs
- `gx commit -m "message"`: Create commits with automatic size checking
- `gx stack`: Analyze and automatically organize changes into logical stacks
- `gx push`: Push changes with upstream branch handling

## Usage Examples

### Basic Workflow

1. Create and set up a new feature branch:
```bash
gx create feature-branch
```

2. Stage and commit changes:
```bash
gx add .
gx commit -m "feat: implement new feature"
```

3. Push your changes:
```bash
gx push
```

### Working with Stacks

When making large changes, `gx stack` helps organize them into manageable stacks:

```bash
# Create a new stack of commits
gx create feature-branch

# Start with your changes
gx commit -m "feat: large feature implementation"

# Create and organize stacks if changes are too large
gx stack

# Work with individual stacks
gx checkout feature-branch-stack-1
gx commit -m "feat: stack 1 changes"
gx push

gx checkout feature-branch-stack-2
gx commit -m "feat: stack 2 changes"
gx push

# Revert stacks if needed by pointing branch to earlier position
git reflog feature-branch
git branch -f feature-branch feature-branch@{1}
```

## Command Reference

`gx create <branch-name> [--stack-threshold N]`
Creates a feature branch with optional size threshold for stacking (default: 300 lines).

`gx add [files]`
Stages files for commit with improved feedback.

`gx commit -m <message> [--force]`
Creates size-checked commits. Use --force to skip checks.

`gx stack`
Analyzes and organizes changes into logical stacks.
- `list`: Shows all current stacks (coming soon)
- `revert`: Removes stacking structure (coming soon)

`gx checkout <branch-name>`
Switches branches with history tracking and safety checks.

`gx push`
Pushes changes with automatic upstream handling.

`gx auth --token <token>`
Sets up authentication for enhanced features. Shoot us an email zach[@]maxium.ai to get your token and stack with no rate limits.


## Contributing

Please refer to guidelines [here](https://github.com/maxium-ai/maxium-cli/blob/master/CONTRIBUTING.md)