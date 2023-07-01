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
# build MVC
from selenium_metaprogramming.view.build import BuildView
from selenium_metaprogramming.controller.build_controller import BuildController

# run MVC
from selenium_metaprogramming.view.run import RunView
from selenium_metaprogramming.model.commands.commands import ScriptCommandMap

# other
from selenium_metaprogramming.view.theme import *

# other libraries
import sys
import traceback
from PyQt5.QtWidgets import *


# --- main ---
class BuilderApp(QMainWindow):
    def __init__(self) -> None:
        # initialize QMainWindow
        super().__init__()

        # style window
        self.setWindowTitle("Selenium Script Builder")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(BACKGROUND_STYLE)

        # create central widget to swap views
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # connect controller actions with view elements
        # build view
        self.build_view = BuildView(ScriptCommandMap.keys())
        self.central_widget.addWidget(self.build_view)

        # run view
        self.run_view = RunView()
        self.central_widget.addWidget(self.run_view)
        self.run_view.run_button.clicked.connect(self.run_script)
        self.run_view.build_button.clicked.connect(self.to_build_view)

        # add controllers
        self.build_controller = BuildController(self)

        # start in build mode
        self.to_build_view()

        # display application
        self.show()

    def to_build_view(self):
        """
        purpose: swap view to builder view and load last script
        """
        print('opening build view')
        self.central_widget.setCurrentWidget(self.build_view)

    def run_script(self):
        """
        purpose: run currently built script
        """
        # get script
        script = self.build_controller.script

        print(f'running {script.name} script')
        try:
            exec(script.compiled_script)
        except Exception as e:
            print(f'failed to run {script.name} due to {type(e)}: {e}\n{traceback.format_exc()}')
        print(f'{script.name} complete')
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
    try:
        App.exec()
    except Exception as e:
        print(f'failed to run app due to {type(e)}: {e}\n{traceback.format_exc()}')
    sys.exit()
