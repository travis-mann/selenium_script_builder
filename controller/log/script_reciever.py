#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""script_receiver.py: intermediary between script and log output for thread safe data transfer"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# --- classes ---
# https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread
class ScriptReceiver(QObject):
    textReceived = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self,queue,*args,**kwargs):
        QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.textReceived.emit(text)
