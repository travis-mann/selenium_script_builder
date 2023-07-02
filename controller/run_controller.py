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
from selenium_metaprogramming.controller.script_worker import ScriptWorker
from selenium_metaprogramming.controller.log.script_reciever import ScriptReceiver
from selenium_metaprogramming.controller.log.queue_stream import WriteStream

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QTextCursor
from queue import Queue


# --- main ---
class RunController:
    def __init__(self, main_window: QMainWindow) -> None:
        self.main_window = main_window

        # connect build view elements to actions
        self.main_window.run_view.run_button.clicked.connect(self.run_script)
        self.main_window.run_view.build_button.clicked.connect(self.to_build_view)

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
        self.main_window.run_view.run_button.setEnabled(False)

        # kill thread
        if self.thread.isRunning():
            self.thread.exit()
            print('script stopped')

    def get_cancel_button(self):
        """
        purpose: switch run button for cancel button
        """
        print('switching run for cancel'),
        self.main_window.run_view.run_button.setEnabled(False),  # disable button before switching function
        self.main_window.run_view.run_button.setText("Cancel"),  # update text to new button function
        self.main_window.run_view.run_button.clicked.disconnect(),  # disconnect script run action
        self.main_window.run_view.run_button.clicked.connect(self.stop_script),  # connect new button action
        self.main_window.run_view.run_button.setEnabled(True),  # re-enable button

    def get_run_button(self):
        """
        purpose: switch cancel button for run button
        """
        print('switching cancel for run'),
        self.main_window.run_view.run_button.setEnabled(False),  # disable button before switching function
        self.main_window.run_view.run_button.setText(f"Run {self.script.name}"),  # update button text to run action
        self.main_window.run_view.run_button.clicked.disconnect(),  # disconnect script cancel action
        self.main_window.run_view.run_button.clicked.connect(self.run_script),  # connect new button action
        self.main_window.run_view.run_button.setEnabled(True),  # re-enable button

    def prepare_script_log(self):
        """
        purpose: handle moving stdout from the script to the log output
        """
        # log action
        print('preparing script log')

        # set up worker and thread
        queue = Queue()
        sys.stdout = WriteStream(queue)
        self.reciever_thread = QThread()
        self.reciever = ScriptReceiver(queue)

        # connect start and end signals
        self.reciever_thread.started.connect(self.reciever.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # connect actions
        self.reciever.textReceived.connect(lambda text: [
                                         print(text),
                                         self.main_window.run_view.log_output.moveCursor(QTextCursor.End),
                                         self.main_window.run_view.log_output.insertPlainText(text),
                                     ])

        # prepare thread
        self.reciever.moveToThread(self.reciever_thread)

    def end_script_log(self):
        """
        purpose: kill receiver and thread
        """
        print('ending script log')
        self.reciever_thread.quit()
        self.reciever.deleteLater()
        self.reciever_thread.deleteLater()

    def run_script(self):
        """
        purpose: run currently built script
        """
        # get script
        self.script = self.main_window.build_controller.script

        # create a script worker and child thread
        self.thread = QThread()
        self.worker = ScriptWorker(self.script)
        self.worker.moveToThread(self.thread)

        # prepare text receiver thread
        self.prepare_script_log()

        # connect signals and slots
        # connect thread start actions
        print('connecting worker thread start actions')
        self.thread.started.connect(
            lambda: [
                # disable switching to build view
                self.main_window.run_view.build_button.setEnabled(False),
                # switch run button to cancel button
                self.get_cancel_button(),
                # start log output receiver
                self.reciever_thread.start(),
                # start script worker
                self.worker.run_script(),
            ]
        )

        print('connecting worker finished actions')
        # end thread and destroy worker when done
        self.thread.finished.connect(
            lambda: [
                self.thread.quit(),
                self.worker.deleteLater(),
            ]
        )

        print('connecting worker thread finished actions')
        # reset gui after thread is done
        self.thread.finished.connect(
            lambda: [
                # delete thread
                self.thread.deleteLater(),
                # re-enable switching to build view
                self.main_window.run_view.build_button.setEnabled(True),
                # switch cancel button back to run button
                self.get_run_button(),
                # end log receiver
                self.end_script_log()
            ]
        )

        # start child thread
        print('starting worker thread')
        self.thread.start()
