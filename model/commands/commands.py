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
from selenium_script_builder.model.commands.click import Click
from selenium_script_builder.model.commands.print import Print
from selenium_script_builder.model.commands.get import Get
from selenium_script_builder.model.commands.sleep import Sleep
from selenium_script_builder.model.commands.send_keys import SendKeys


# --- classes ---
ScriptCommandMap = {command.name: command for command in [Get, Click, Print, Sleep, SendKeys]}
