#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""command.py: Parent class for script commands"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from typing import List, Tuple


# --- classes ---
class Command:
    """
    purpose: parent class for commands
    """
    def __init__(self):
        self.args = []

    def compile(self) -> Tuple[str, List[str]]:
        """
        purpose: create python code associated with command as a string
                 along with a list of associated import commands.
        :return command_str: python code to execute command
        :return import_strs: list of associated import commands
        """
        NotImplementedError(f'compile method not implemented for {self.__class__.__name__}')

    def validate(self, args: List[str]) -> bool:
        """
        purpose: check if the given args are valid for the command
        :param args: user entered arguments for command
        :return is_valid: bool representing if the args are valid for the command
        """
        NotImplementedError(f'validate method not implemented for {self.__class__.__name__}')
