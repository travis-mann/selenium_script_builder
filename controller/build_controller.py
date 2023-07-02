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
        self.row_to_move_original_index = None

        # connect build view elements to actions
        self.main_window.build_view.compile_button.clicked.connect(self.compile_script)
        self.main_window.build_view.clear_button.clicked.connect(self.clear_script)
        self.main_window.build_view.add_button.clicked.connect(self.add_command)
        self.main_window.build_view.remove_button.clicked.connect(self.remove_command)
        self.main_window.build_view.commands_dropdown.currentTextChanged.connect(self.update_hint)
        self.main_window.build_view.commands_dropdown.currentTextChanged.connect(self.reset_args)
        self.main_window.build_view.command_list.model().rowsAboutToBeMoved.connect(self.get_row_to_move)
        self.main_window.build_view.command_list.model().rowsMoved.connect(self.update_command_order)

        # initialization commands
        self.update_hint()

    def to_run_view(self) -> None:
        """
        purpose: switch to run view and run currently built script
        """
        # log action
        print('opening run view')

        # update script button name
        self.main_window.run_view.run_button.setText(f"Run {self.script.name}")

        # switch views
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

            # reset formatting and relevant fields
            self.reset_args()
            self.main_window.build_view.command_list.setProperty('warning', False)
            self.main_window.build_view.command_list.style().unpolish(self.main_window.build_view.command_list)
            self.main_window.build_view.command_list.style().polish(self.main_window.build_view.command_list)
        else:  # invalid args
            self.main_window.build_view.args_field.setProperty('warning', True)
            self.main_window.build_view.args_field.style().unpolish(self.main_window.build_view.args_field)
            self.main_window.build_view.args_field.style().polish(self.main_window.build_view.args_field)

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
        # get selected index from ui
        selected_indexes = [item.row() for item in self.main_window.build_view.command_list.selectedIndexes()]

        # remove command from script
        # remove in reverse order by index to maintain placement for lower indexes
        for command_index in sorted(selected_indexes, reverse=True):
            self.script.remove_command(command_index)

        # update command list
        self.update_command_list()

    def update_command_list(self) -> None:
        """
        purpose: update command list with current script commands
        """
        print('updating command list display')

        # clear list
        self.main_window.build_view.command_list.clear()

        # add all current commands
        for command in self.script.commands:
            cmd_str = self.get_command_str(command)
            self.main_window.build_view.command_list.addItem(cmd_str)

    def get_row_to_move(self):
        """
        purpose: store original index for row to move
        """
        self.row_to_move_original_index = self.main_window.build_view.command_list.selectedIndexes()[0].row()

    def update_command_order(self):
        """
        purpose: update script when commands are swapped in the UI
        """
        # log action
        print('updating script command order')

        # get new command index
        row_to_move_new_index = self.main_window.build_view.command_list.selectedIndexes()[0].row()

        # move command from stored old index to new index
        command = self.script.commands.pop(self.row_to_move_original_index)
        self.script.commands.insert(row_to_move_new_index, command)

        # log action
        print(f'moved {command.name} command from index {self.row_to_move_original_index} to {row_to_move_new_index}')

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
            self.main_window.build_view.command_list.setProperty('warning', True)
            self.main_window.build_view.command_list.style().unpolish(self.main_window.build_view.command_list)
            self.main_window.build_view.command_list.style().polish(self.main_window.build_view.command_list)

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
        self.main_window.build_view.args_field.setProperty('warning', False)
        self.main_window.build_view.args_field.style().unpolish(self.main_window.build_view.args_field)
        self.main_window.build_view.args_field.style().polish(self.main_window.build_view.args_field)