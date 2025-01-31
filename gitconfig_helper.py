# Dependencies: rich
# To install dependencies, run: python -m pip install rich
# To test that rich is installed, run: python -m rich

import sys
from dependency_installer import check_and_install_dependencies

# Check and install dependencies
check_and_install_dependencies({'rich'})

from rich.console import Console
from rich.table import Table

def print_aliases():
    console = Console()
    table = Table(title="Git Aliases", show_lines=True, header_style="bold yellow")

    table.add_column("Alias", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")

    aliases = [
        ("alias", "List all aliases"),
        ("branches", "Track all remote branches"),
        ("cleanup", "Cleanup merged branches"),
    ]

    # Sort aliases by alias name
    aliases.sort()

    for alias, description in aliases:
        table.add_row(alias, description)

    console.print(table)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "print_aliases":
            print_aliases()
        else:
            print(f"Function {function_name} not found.")
    else:
        print("No function name provided.")