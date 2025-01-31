import sys
import subprocess
import importlib.metadata

def check_and_install_dependencies(required):
    installed = {pkg.metadata['Name'] for pkg in importlib.metadata.distributions()}
    missing = required - installed

    if missing:
        print(f"Missing dependencies: {missing}. Installing...")
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
