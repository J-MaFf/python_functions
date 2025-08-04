# Dependencies: rich
# To install dependencies, run: python -m pip install rich
# To test that rich is installed, run: python -m rich

import sys
import subprocess
import re

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("The 'rich' library is not installed. Attempting to install it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.table import Table

def get_git_aliases():
    """Dynamically fetch all git aliases from git config."""
    # Human-readable descriptions for known aliases
    alias_descriptions = {
        "alias": "List all git aliases in a formatted table",
        "branches": "Download all remote branches and create local tracking branches",
        "cleanup": "Delete local branches that no longer exist on the remote (only merged branches are deleted)"
    }

    try:
        # Get all aliases from git config
        result = subprocess.run(['git', 'config', '--get-regexp', 'alias'],
                              capture_output=True, text=True, check=True)

        aliases = []
        for line in result.stdout.strip().split('\n'):
            if line:
                # Parse "alias.name value" format
                match = re.match(r'alias\.(.+?)\s+(.+)', line)
                if match:
                    alias_name = match.group(1)
                    alias_value = match.group(2)

                    # Use custom description if available, otherwise show the command
                    if alias_name in alias_descriptions:
                        description = alias_descriptions[alias_name]
                    elif alias_value.startswith('!'):
                        # For shell commands, show a cleaned up version
                        command = alias_value[1:]
                        if len(command) > 80:
                            description = f"Shell: {command[:77]}..."
                        else:
                            description = f"Shell: {command}"
                    else:
                        # For git sub-commands, show as-is but truncate if too long
                        if len(alias_value) > 80:
                            description = alias_value[:77] + "..."
                        else:
                            description = alias_value

                    aliases.append((alias_name, description))

        return sorted(aliases)
    except subprocess.CalledProcessError:
        return [
            ("alias", "List all aliases"),
            ("branches", "Track all remote branches"),
            ("cleanup", "Cleanup merged branches"),
        ]

def print_aliases():
    console = Console()
    table = Table(title="Git Aliases", show_lines=True, header_style="bold yellow")

    table.add_column("Alias", justify="left", style="cyan", no_wrap=True)
    table.add_column("Command/Description", justify="left", style="magenta")

    aliases = get_git_aliases()

    for alias, description in aliases:
        table.add_row(alias, description)

    console.print(table)
    console.print(f"\n[dim]Found {len(aliases)} git aliases[/dim]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "print_aliases":
            print_aliases()
        else:
            print(f"Function {function_name} not found.")
    else:
        print("No function name provided.")