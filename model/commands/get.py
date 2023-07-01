#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""get.py: command to go to url"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"

# --- imports ---
from selenium_metaprogramming.model.commands.command import Command

import validators
from typing import List, Tuple


# --- classes ---
class Get(Command):
    """
    purpose: click element by xpath
    """
    name = 'Get'
    hint = 'URL'

    def __init__(self):
        super(Get, self).__init__()

    def compile(self) -> Tuple[str, List[str]]:
        command = f"driver.get('{self.args[0]}')"
        imports = []
        return command, imports

    def validate(self, args: List[str]) -> bool:
        # check only 1 arg given
        if len(args) != 1:
            print(f'arg validation failure: {self.name} command accepts 1 arg, received {len(args)}')
            return False

        # check if arg is a valid url
        # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
        if validators.url(args[0]):
            return True
        print(f'arg validation failure: {self.name} command received invalid url: {args[0]}')
        return False

