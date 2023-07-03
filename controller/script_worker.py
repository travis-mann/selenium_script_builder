#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""script_worker.py: Worker class to run compiled scripts on a child thread"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from selenium_metaprogramming.model.script import Script

import traceback
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# --- classes ---
class ScriptWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, script: Script):
        super(ScriptWorker, self).__init__()
        self.script = script

    @pyqtSlot()
    def run_script(self):
        """run compiled python script"""
        # log action
        print(f'running {self.script.name} script')

        # attempt to run
        try:
            exec(self.script.compiled_script)
        except Exception as e:
            print(f'failed to run {self.script.name} due to {type(e)}: {e}\n{traceback.format_exc()}')

        # emit complete signal
        print(f'{self.script.name} complete')
        self.finished.emit()
