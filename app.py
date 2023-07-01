#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""app.py: interactive gui for creating selenium scripts"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium_metaprogramming.view.build import BuildView
from selenium_metaprogramming.view.run import RunView

from PyQt5.QtWidgets import *
import sys


# --- main ---
class BuilderApp(QMainWindow):
    def __init__(self) -> None:
        # initialize QMainWindow
        super().__init__()

        # set title
        self.setWindowTitle("Selenium Metaprogramming")

        # set window geometry
        self.setGeometry(100, 100, 600, 400)

        # create central widget to swap views
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # connect actions to views and store
        # build view
        self.build_view = BuildView(['Click', 'Send Keys', 'Get', 'Sleep'])
        self.central_widget.addWidget(self.build_view)
        self.build_view.compile_button.clicked.connect(self.compile_script)

        # run view
        self.run_view = RunView()
        self.central_widget.addWidget(self.run_view)
        self.run_view.run_button.clicked.connect(self.run_script)
        self.run_view.build_button.clicked.connect(self.to_build_view)

        # start in build mode
        self.to_build_view()

        # display application
        self.show()

    def to_run_view(self):
        """
        purpose: switch to run view and run currently built script
        """
        print('opening run view')
        self.central_widget.setCurrentWidget(self.run_view)

    def to_build_view(self):
        """
        purpose: swap view to builder view and load last script
        """
        print('opening build view')
        self.central_widget.setCurrentWidget(self.build_view)

    def compile_script(self):
        """
        purpose: compile currently built script
        """
        # compile script to run
        print('compiling current script')

        # convert stored commands into python code
        # store code in an output folder
        # script runner will grab most recent script

        # move to run view
        self.to_run_view()

    def run_script(self):
        """
        purpose: run currently built script
        """
        print('running current script')

        # spawn a thread to run the script
        # pipe stdout back into log output
        # disable buttons until complete
        # potentially add a cancel button


# --- main ---
if __name__ == "__main__":
    # create PyQT app
    App = QApplication(sys.argv)

    # create window instance
    G = BuilderApp()

    # start app
    sys.exit(App.exec())
