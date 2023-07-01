#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""command.py: Enum of valid script commands"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from enum import Enum
from selenium_metaprogramming.model.commands.click import Click
from selenium_metaprogramming.model.commands.print import Print
from selenium_metaprogramming.model.commands.get import Get
from selenium_metaprogramming.model.commands.sleep import Sleep


# --- classes ---
ScriptCommandMap = {command.name: command for command in [Get, Click, Print, Sleep]}
