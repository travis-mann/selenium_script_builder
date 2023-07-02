#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""queue_stream.py: pipes stdout into a queue"""


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
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)
