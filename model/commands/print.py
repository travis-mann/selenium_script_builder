#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""print.py: command to call python print function"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"

# --- imports ---
from selenium_script_builder.model.commands.command import Command

from typing import List, Tuple


# --- classes ---
class Print(Command):
    """
    purpose: print given string
    """
    name = 'Print'
    hint = 'Str'

    def __init__(self):
        super(Print, self).__init__()

    def compile(self) -> Tuple[str, List[str]]:
        arg_str = "'" + "', '".join(self.args) + "'"
        command_str = f"print({arg_str})"
        imports = []
        return command_str, imports

    def validate(self, args: List[str]) -> bool:
        return True
