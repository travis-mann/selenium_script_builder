#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""script.py: script model for data layer logic"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium_metaprogramming.model.commands.command import Command

from typing import List


# --- classes ---
class Script:
    """
    purpose: Model to represent script
    """
    def __init__(self):
        # params from args
        self.name = None

        # syntax - command: [args]
        self.commands = []

        # track if script needs to be compiled
        self.compiled = False

        # store compiled script
        self.compiled_script = ''

    def compile(self) -> str:
        """
        purpose: convert loaded commands to executable Python code
        """
        # check for > 0 commands
        if not self.commands:
            raise ValueError('Please enter at least 1 command')

        # collect commands and associated imports
        command_strs = []
        import_strs = []

        # iterate over all commands
        for command in self.commands:
            print(f'compiling {command.name} command')
            command_str, import_str = command.compile()

            # store command
            command_strs.append(command_str)

            # don't add import if it has already been added
            if import_str not in import_strs:
                import_strs += import_str

        # store compiled commands in a string
        python_code = self.start_script(import_strs)

        # add commands
        for command_str in command_strs:
            python_code += f'{command_str}\n'

        # add final commands
        python_code += self.end_script()

        # show output
        print(f'compiled code:\n{python_code}')
        self.compiled = True
        self.compiled_script = python_code

    def add_command(self, command: Command, args: list = []) -> None:
        print(f'adding command: {command.name}')

        # build command
        command.args = args

        # store command
        self.commands.append(command)

        # log success
        print(f'{command.name} successfully added to script')
        self.compiled = False

    def remove_command(self, idx: int) -> None:
        # log action
        print(f'removing {self.commands[idx].name} command at index {idx}')

        # remove item at given index
        del self.commands[idx]

        # reset compiled tracker since script was updated
        self.compiled = False

        # log success
        print('command removed')

    def start_script(self, import_strs: List[str]) -> str:
        """
        purpose: code to add before any selenium commands
        :return preamble: initial code required before adding commands
        """
        # format imports
        custom_imports = '\n'.join(import_strs)

        return f"""# imports
import chromedriver_autoinstaller
from selenium import webdriver
{custom_imports}

# create drivers
driver = webdriver.Chrome()
driver.maximize_window()

# commands
"""

    def end_script(self) -> str:
        """
        purpose: commands required to end a selenium script
        """
        return """driver.quit()"""