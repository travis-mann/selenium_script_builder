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
from selenium_metaprogramming.view.build_view import BuildView
from selenium_metaprogramming.controller.build_controller import BuildController

# run MVC
from selenium_metaprogramming.view.run_view import RunView
from selenium_metaprogramming.controller.run_controller import RunController

# other
from selenium_metaprogramming.view.theme import *
from selenium_metaprogramming.model.commands.commands import ScriptCommandMap

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
        self.setFixedSize(600, 400)
        self.setStyleSheet(STYLE)


        # create central widget to swap views
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # build view
        self.build_view = BuildView(ScriptCommandMap.keys())
        self.central_widget.addWidget(self.build_view)

        # run view
        self.run_view = RunView()
        self.central_widget.addWidget(self.run_view)

        # add controllers
        self.build_controller = BuildController(self)
        self.run_controller = RunController(self)

        # start in build mode
        self.run_controller.to_build_view()

        # display application
        self.show()


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
