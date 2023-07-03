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
from PyQt5.QtCore import QThread, pyqtSlot
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
        if self.worker_thread.isRunning():
            self.worker_thread.exit()
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

    def start_script_log(self):
        """
        purpose: handle moving stdout from the script to the log output
        """
        # log action
        print('preparing script log')

        # set up worker and thread
        queue = Queue()
        self.receiver_thread = QThread()
        self.receiver = ScriptReceiver(queue)

        # track original stdout to reset after receiver is finished
        original_stdout = sys.stdout

        # connect actions
        self.receiver.textReceived.connect(lambda text: [
            self.main_window.run_view.log_output.moveCursor(QTextCursor.End),
            self.main_window.run_view.log_output.insertPlainText(text)
        ])

        # connect start and end signals
        self.receiver_thread.started.connect(lambda: self.set_std_out(WriteStream(queue)))
        self.receiver_thread.started.connect(self.receiver.run)  # run stdout receiver
        self.receiver.finished.connect(self.receiver.deleteLater)  # delete receiver worker
        self.receiver.finished.connect(self.receiver_thread.quit)  # signal thread to end
        self.receiver.finished.connect(lambda: self.set_std_out(original_stdout))  # reset std out
        self.receiver_thread.finished.connect(self.receiver_thread.deleteLater)  # delete receiver thread

        # prepare thread
        self.receiver.moveToThread(self.receiver_thread)
        self.receiver_thread.start()

    def set_std_out(self, new_std_out):
        sys.stdout = new_std_out

    @pyqtSlot()
    def start_script_thread(self):
        # get script
        self.script = self.main_window.build_controller.script

        # create a script worker and child thread
        self.worker_thread = QThread()
        self.worker = ScriptWorker(self.script)
        self.worker.moveToThread(self.worker_thread)

        # connect worker thread start actions
        self.worker_thread.started.connect(lambda: self.main_window.run_view.build_button.setEnabled(False))  # disable to build button
        self.worker_thread.started.connect(self.get_cancel_button)  # swap run for cancel
        self.worker_thread.started.connect(self.receiver_thread.start)  # start pipe to QTextEdit window
        self.worker_thread.started.connect(self.worker.run_script)  # run script

        # connect worker end actions
        self.worker.finished.connect(self.worker_thread.quit)  # delete thread
        self.worker.finished.connect(self.worker.deleteLater)  # delete worker
        self.worker.finished.connect(self.receiver.finished.emit)  # end pipe to QTextEdit window

        # connect worker thread end actions
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)  # delete thread
        self.worker_thread.finished.connect(lambda: self.main_window.run_view.build_button.setEnabled(True))  # re-enable to build button
        self.worker_thread.finished.connect(self.get_run_button)  # swap cancel for run

        # start thread
        print('starting worker thread')
        self.worker_thread.start()

    def run_script(self):
        """
        purpose: run currently built script
        """
        self.start_script_log()
        self.start_script_thread()
