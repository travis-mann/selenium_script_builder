#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""run.py: run view widget for application"""


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
class RunView(QWidget):
    """
    purpose: GUI view while running a script
    """
    def __init__(self):
        super().__init__()

        # create layout
        layout = QVBoxLayout()

        # add run button
        self.run_button = QPushButton("Run Script")
        layout.addWidget(self.run_button)

        # add cancel button
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.cancel_button)

        # add log window
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # add build button
        self.build_button = QPushButton("Build")
        layout.addWidget(self.build_button)

        # package
        self.setLayout(layout)
