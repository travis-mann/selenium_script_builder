#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""run_view.py: run view widget for application"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium_metaprogramming.view.theme import *
from PyQt5.QtWidgets import *


# --- classes ---
class RunView(QWidget):
    """
    purpose: GUI view while running a script
    """
    def __init__(self):
        super().__init__()

        # create layout
        layout = QVBoxLayout()

        # add run button
        self.run_button = QPushButton()  # button text updated when switching views
        self.run_button.setStyleSheet(STYLE)
        layout.addWidget(self.run_button)

        # add log window
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # add build button
        self.build_button = QPushButton("Build")
        self.build_button.setStyleSheet(STYLE)
        layout.addWidget(self.build_button)

        # package
        self.setLayout(layout)
