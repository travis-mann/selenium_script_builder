#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""click.py: command to click element by xpath"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"

# --- imports ---
from selenium_metaprogramming.model.commands.command import Command

import lxml.etree
import json
from typing import List, Tuple


# --- classes ---
class Click(Command):
    """
    purpose: click element by xpath
    """
    name = 'Click'
    hint = 'XPATH'

    def __init__(self):
        super(Click, self).__init__()

    def compile(self) -> Tuple[str, List[str]]:
        # https://stackoverflow.com/questions/18886596/replace-all-quotes-in-a-string-with-escaped-quotes
        command = f"driver.find_element(By.XPATH, {json.dumps(self.args[0])}).click()"
        imports = ['from selenium.webdriver.common.by import By']
        return command, imports

    def validate(self, args: List[str]) -> bool:
        # check only 1 arg given
        if len(args) != 1:
            print(f'arg validation failure: {self.name} command accepts 1 arg, received {len(args)}')
            return False

        # https://stackoverflow.com/questions/50151904/xpath-syntax-validator-in-python
        try:
            lxml.etree.XPath(args[0])
            return True
        except lxml.etree.XPathSyntaxError:
            print(f'arg validation failure: {self.name} command received invalid XPATH {args[0]}')
            return False
