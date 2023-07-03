#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""sleep.py: command to call python sleep function"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"

# --- imports ---
from selenium_script_builder.model.commands.command import Command

from time import sleep
from typing import List, Tuple


# --- classes ---
class Sleep(Command):
    """
    purpose: print given string
    """
    name = 'Sleep'
    hint = 'Int (Seconds)'

    def __init__(self):
        super(Sleep, self).__init__()

    def compile(self) -> Tuple[str, List[str]]:
        command = f"sleep({self.args[0]})"
        imports = ['from time import sleep']
        return command, imports

    def validate(self, args: List[str]) -> bool:
        # check only 1 arg given
        if len(args) != 1:
            print(f'arg validation failure: {self.name} command accepts 1 arg, received {len(args)}')
            return False

        # check that string can be converted to int
        try:
            int(args[0])
            return True
        except ValueError:
            print(f'arg validation failure: {self.name} command requires an integer, received {len(args)}')
            return False
