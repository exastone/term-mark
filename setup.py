import os
import shutil
from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    # Post-installation compies functionality from tm_functions.py init() such that user no longer 
    # has to manually run `term-mark --init` after installation
    def run(self):
        install.run(self)
        try:
            line_to_append = 'source "$HOME/.config/zsh/zsh_functions/tm.zsh"'

            # check if shell function is already sourced to .zshrc
            zshrc_path = os.path.expanduser('~/.zshrc')
            line_exists = any(line_to_append in line for line in open(zshrc_path))
            if not line_exists:
                # Append line to .zshrc
                with open(zshrc_path, 'a') as zshrc_file:
                    zshrc_file.write('\n' + line_to_append + '\n')

            # Copy file tm shell function
            # Get the directory of the calling script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct source and destination paths
            source_file = os.path.join(script_dir, "term_mark", "tm.zsh")
            destination_folder = os.path.expanduser("~/.config/zsh/zsh_functions")
            destination_file = os.path.join(destination_folder, "tm.zsh")

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            if os.path.exists(source_file):
                shutil.copy(source_file, destination_file)
            else:
                print(f"Source file {source_file} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

setup(
    name="term-mark",
    version="0.1.4",
    author="Andrew Stone",
    packages=[
        "term_mark",
        "term_mark.InquirerPy.InquirerPy",
        "term_mark.InquirerPy.InquirerPy.base",
        "term_mark.InquirerPy.InquirerPy.containers",
        "term_mark.InquirerPy.InquirerPy.prompts"
    ],
    description="Bookmark directories and jump to them quickly",
    entry_points={
        "console_scripts": [
            "term-mark = term_mark.main:main",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
)