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
from selenium_script_builder.model.commands.command import Command

import lxml.etree
import json
from typing import List, Tuple


# --- classes ---
class SendKeys(Command):
    """
    purpose: click element by xpath
    """
    name = 'Send Keys'
    hint = 'XPATH; Str/Keys.KEY_NAME'

    def __init__(self):
        super(SendKeys, self).__init__()

    def compile(self) -> Tuple[str, List[str]]:
        # start imports list
        imports = ['from selenium.webdriver.common.by import By']

        # check if send_keys arg is a string or key
        if 'Keys.' in self.args[1]:
            send_keys_arg = self.args[1]
            imports.append('from selenium.webdriver.common.keys import Keys')
        else:
            send_keys_arg = json.dumps(self.args[1])

        # https://stackoverflow.com/questions/18886596/replace-all-quotes-in-a-string-with-escaped-quotes
        command = f"driver.find_element(By.XPATH, {json.dumps(self.args[0])}).send_keys({send_keys_arg})"

        return command, imports

    def validate(self, args: List[str]) -> bool:
        # check only 1 arg given
        if len(args) != 2:
            print(f'arg validation failure: {self.name} command accepts 2 args, received {len(args)}')
            return False

        # https://stackoverflow.com/questions/50151904/xpath-syntax-validator-in-python
        try:
            lxml.etree.XPath(args[0])
            return True
        except lxml.etree.XPathSyntaxError:
            print(f'arg validation failure: {self.name} command received invalid XPATH {args[0]}')
            return False
