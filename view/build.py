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
from typing import Dict
from PyQt5.QtWidgets import *
import sys


# --- classes ---
class BuildView(QWidget):
    """
    purpose: GUI view while running a script
    """

    def __init__(self, commands: list):
        super().__init__()

        # create layout
        layout = QVBoxLayout()

        # script title field
        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText('Script Title')
        layout.addWidget(self.title_field)

        # clear button
        self.clear_button = QPushButton("Clear Script")
        layout.addWidget(self.clear_button)

        # remove command button
        self.remove_button = QPushButton("-")
        layout.addWidget(self.remove_button)

        # commands dropdown
        self.commands_dropdown = QComboBox()
        for command in commands:
            self.commands_dropdown.addItem(command)
        layout.addWidget(self.commands_dropdown)

        # add command button
        self.add_button = QPushButton("+")
        layout.addWidget(self.add_button)

        # run button
        self.compile_button = QPushButton("Compile Script")
        layout.addWidget(self.compile_button)

        # script window
        self.command_list = QListView()
        layout.addWidget(self.command_list)

        # package
        self.setLayout(layout)


