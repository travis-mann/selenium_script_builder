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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from selenium_metaprogramming.script_worker import ScriptWorker


# --- main ---
class RunController:
    def __init__(self, main_window: QMainWindow) -> None:
        self.main_window = main_window

        # connect build view elements to actions
        self.main_window.run_view.run_button.clicked.connect(self.run_script)
        self.main_window.run_view.build_button.clicked.connect(self.to_build_view)
        self.main_window.run_view.cancel_button.clicked.connect(self.stop_script)

    def to_build_view(self):
        """
        purpose: swap view to builder view and load last script
        """
        print('opening build view')
        self.main_window.central_widget.setCurrentWidget(self.main_window.build_view)

    def stop_script(self):
        """
        purpose: kill child thread running script
        """
        # log action
        print('stopping script')

        # disable multiple cancel inputs
        self.main_window.run_view.cancel_button.setEnabled(False)

        # kill thread
        if self.thread.isRunning():
            self.thread.exit()
            print('script stopped')

    def run_script(self):
        """
        purpose: run currently built script
        """
        # get script
        script = self.main_window.build_controller.script

        # create a script worker and child thread
        self.thread = QThread()
        self.worker = ScriptWorker(script)
        self.worker.moveToThread(self.thread)

        # connect signals and slots
        self.thread.started.connect(self.worker.run_script)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # disable/ enable buttons with script start and finish
        self.thread.started.connect(
            lambda: [
            self.main_window.run_view.run_button.setEnabled(False),
            self.main_window.run_view.build_button.setEnabled(False),
            self.main_window.run_view.cancel_button.setEnabled(True),
            ]
        )

        # connect resets after script complete
        self.thread.finished.connect(
            lambda: [
            self.main_window.run_view.run_button.setEnabled(True),
            self.main_window.run_view.build_button.setEnabled(True),
            self.main_window.run_view.cancel_button.setEnabled(False),
            ]
        )

        # start child thread
        print('starting child thread')
        self.thread.start()
        print(self.thread.isRunning())
        print('child thread done')
