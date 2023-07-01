#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""build.py: build view widget for application"""

# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"

# --- imports ---
from selenium_metaprogramming.view.theme import *

from typing import List
from PyQt5.QtWidgets import *


# --- classes ---
class BuildView(QWidget):
    """
    purpose: GUI view while running a script
    """

    def __init__(self, command_names: List[str]):
        super().__init__()

        # create layout
        self.layout = QVBoxLayout()

        # add main widgets
        self.add_header_widget(command_names)
        self.add_body_widget()

        # package
        self.setLayout(self.layout)

    def add_header_widget(self, command_names: List[str]) -> None:
        """
        purpose: add header widget for title and command addition
        """
        # body layout/widget
        header_layout = QVBoxLayout()
        header_widget = QWidget()

        # script title field
        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText('Script Title')
        self.title_field.setStyleSheet(LINE_EDIT_STYLE)
        header_layout.addWidget(self.title_field)

        # command add widget
        header_layout.addWidget(self.get_command_add_widget(command_names))

        # package and add
        header_widget.setLayout(header_layout)
        self.layout.addWidget(header_widget)

    def add_body_widget(self) -> None:
        """
        purpose: UI main body
        """
        # body layout/widget
        body_layout = QHBoxLayout()
        body_widget = QWidget()

        # add menu
        body_layout.addWidget(self.get_menu_widget())

        # script window
        self.command_list = QListWidget()
        self.command_list.setStyleSheet(DISPLAY_STYLE)
        self.command_list.setSelectionMode(QAbstractItemView.MultiSelection)
        body_layout.addWidget(self.command_list)

        # package and add
        body_widget.setLayout(body_layout)
        self.layout.addWidget(body_widget)

    def get_command_add_widget(self, command_names: List[str]) -> QWidget:
        """
        purpose: create and format command dropdown, arg lineedit and add button
        :return command_add_widget: widget with command dropdown, arg lineedit and add button
        """
        # layout/widget for commands, args & add command button
        command_add_widget = QWidget()

        command_add_layout = QHBoxLayout()
        command_definition_widget = QWidget()

        command_definition_layout = QVBoxLayout()

        # commands dropdown
        self.commands_dropdown = QComboBox()
        for command_name in command_names:
            self.commands_dropdown.addItem(command_name)
        self.commands_dropdown.setStyleSheet(DROPDOWN_STYLE)
        command_definition_layout.addWidget(self.commands_dropdown)

        # args lineedit
        self.arg_label = QLabel('Arguments (comma separated)')
        self.args_field = QLineEdit()
        self.args_field.setStyleSheet(LINE_EDIT_STYLE)
        command_definition_layout.addWidget(self.args_field)
        command_definition_widget.setLayout(command_definition_layout)
        command_definition_widget.setStyleSheet(MENU_BACKGROUND_STYLE)
        command_add_layout.addWidget(command_definition_widget)

        # add command button
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet(BUTTON_STYLE)
        command_add_layout.addWidget(self.add_button)
        command_add_widget.setLayout(command_add_layout)
        command_add_widget.setStyleSheet(MENU_BACKGROUND_STYLE)

        # output final widget
        return command_add_widget

    def get_menu_widget(self) -> QWidget:
        """
        purpose: construct menu with various buttons
        """
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()

        # run button
        self.compile_button = QPushButton("Compile Script")
        self.compile_button.setStyleSheet(BUTTON_STYLE)
        menu_layout.addWidget(self.compile_button)

        # remove button
        self.remove_button = QPushButton("Remove Command")
        self.remove_button.setStyleSheet(BUTTON_STYLE)
        menu_layout.addWidget(self.remove_button)

        # clear button
        self.clear_button = QPushButton("Clear Script")
        self.clear_button.setStyleSheet(BUTTON_STYLE)
        menu_layout.addWidget(self.clear_button)

        # package and return
        menu_widget.setLayout(menu_layout)
        menu_widget.setStyleSheet(MENU_BACKGROUND_STYLE)
        return menu_widget
