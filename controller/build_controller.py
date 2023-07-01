#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""build_controller.py: controller logic for build actions"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium_metaprogramming.model.script import Script
from selenium_metaprogramming.model.commands.click import Command
from selenium_metaprogramming.model.commands.commands import ScriptCommandMap
from selenium_metaprogramming.view.theme import *

import traceback
from typing import List
from PyQt5.QtWidgets import *


# --- main ---
class BuildController:
    def __init__(self, main_window: QMainWindow) -> None:
        self.main_window = main_window
        self.script = Script()

        # connect build view elements to actions
        self.main_window.build_view.compile_button.clicked.connect(self.compile_script)
        self.main_window.build_view.clear_button.clicked.connect(self.clear_script)
        self.main_window.build_view.add_button.clicked.connect(self.add_command)
        self.main_window.build_view.remove_button.clicked.connect(self.remove_command)
        self.main_window.build_view.commands_dropdown.currentTextChanged.connect(self.update_hint)
        self.main_window.build_view.commands_dropdown.currentTextChanged.connect(self.reset_args)

        # initialization commands
        self.update_hint()

    def to_run_view(self) -> None:
        """
        purpose: switch to run view and run currently built script
        """
        print('opening run view')
        self.main_window.central_widget.setCurrentWidget(self.main_window.run_view)

    def add_command(self) -> None:
        """
        purpose: add selected command in ui to script model and update view
        """
        print('adding command')

        # get command from ui
        command_to_add = self.get_command()
        args = self.get_args()

        # validate args
        if command_to_add.validate(args):
            # add command to script
            self.script.add_command(command_to_add, args)
            self.reset_args()
        else:  # invalid args
            self.main_window.build_view.args_field.setStyleSheet(LINE_EDIT_ERROR_STYLE)

        # update command list
        self.update_command_list()

    def get_args(self) -> List[str]:
        """
        purpose: get a list of the user entered args
        """
        return self.main_window.build_view.args_field.text().split('; ')

    def get_command(self) -> Command:
        """
        purpose: resolve currently selected command name to a command
        :return command:
        """
        # get currently selected command name
        command_name = self.main_window.build_view.commands_dropdown.currentText()

        # resolve command name to a command
        try:
            command = ScriptCommandMap[command_name]()
        except IndexError as e:
            print(f'{command_name} not found in ScriptCommandMap')
            raise e

        return command

    def remove_command(self) -> None:
        """
        purpose: remove selected command in ui from the script model and update view
        """
        # get command from ui
        commands_to_remove = self.main_window.build_view.command_list.selectedItems()
        print(f'commands to remove: {commands_to_remove.text()}')

        # add command to script
        # self.script.remove_command(command_to_remove)

        # update command list
        # self.update_command_list()

    def update_command_list(self) -> None:
        """
        purpose: update command list with current script commands
        """
        print('updating command list')

        # clear list
        self.main_window.build_view.command_list.clear()

        # add all current commands
        for command in self.script.commands:
            cmd_str = self.get_command_str(command)
            self.main_window.build_view.command_list.addItem(cmd_str)

    def get_command_str(self, command: Command) -> str:
        """
        purpose: convert a comand into a string for display
        :param command: script command
        :param args: command arguments
        :return:
        """
        return f'{command.name}({", ".join(command.args)})'

    def compile_script(self):
        """
        purpose: compile currently built script
        """
        # compile script to run
        print('compiling current script')

        # set script name
        self.script.name = self.main_window.build_view.title_field.text()

        try:
            # convert script commands to python
            self.script.compile()

            # convert stored commands into python code
            # potentially store code in an output folder
            # script runner could grab most recent script

            # move to run view
            self.to_run_view()
        except Exception as e:
            print(f'failed to compile script due to {type(e)}: {e}\n{traceback.format_exc()}')

    def clear_script(self):
        """
        purpose: create new script instance to reset settings
        """
        print('clearing script')

        # open confirmation window
        # ...

        # create new script instance
        self.script = Script()

        # update command list
        self.update_command_list()

    def update_hint(self):
        """
        purpose: update arg hint from currently selected command
        """
        # get current selected command
        current_command_name = self.main_window.build_view.commands_dropdown.currentText()

        # get hint associated with command name
        hint = ScriptCommandMap[current_command_name].hint

        # update arg hint
        self.main_window.build_view.args_field.setPlaceholderText(hint)

    def reset_args(self):
        """
        purpose: reset args field
        """
        # clear field
        self.main_window.build_view.args_field.clear()

        # reset style
        self.main_window.build_view.args_field.setStyleSheet(LINE_EDIT_STYLE)