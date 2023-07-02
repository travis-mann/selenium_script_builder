#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""theme.py: style settings for views"""


# --- metadata ---
__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
# N/A


# --- main ---
FONT_COLOR = '#989898'
TEXT_BACKGROUND_COLOR = '#2e3033'
BACKGROUND_COLOR = '#36454F'
FONT_SIZE = 15

NO_WARNING_STYLE = "border: 1px solid transparent;"
WARNING_STYLE = "border: 1px solid red;"

DROPDOWN_STYLE = f"""
background-color: {TEXT_BACKGROUND_COLOR};
color: white;
border-radius:3px;
font:bold {FONT_SIZE}px;
"""

STYLE = f"""
*[warning="false"] {{{NO_WARNING_STYLE}}}
*[warning="true"] {{{WARNING_STYLE}}}

QMainWindow {{
    background-color: {BACKGROUND_COLOR};
}}
QPushButton {{
    background-color:transparent;
    font:bold {FONT_SIZE}px;
    color: {FONT_COLOR};
    text-align: center;
}}
QPushButton#menuButton {{
    text-align: left;
}}
QPushButton:hover {{
    font:bold {FONT_SIZE+1}px;
    color: white;
}}
QLineEdit {{
    background-color:{TEXT_BACKGROUND_COLOR};
    border-radius:3px;
    color: white;
    font: {FONT_SIZE}px;
    border: 1px solid transparent;
}}
QListWidget {{
    color:white;
    font:bold {FONT_SIZE}px;
    background-color:{TEXT_BACKGROUND_COLOR};
}}
QTextEdit {{
    background-color:{TEXT_BACKGROUND_COLOR};
    border-radius:3px;
    color: white;
    font: {FONT_SIZE}px;
    border: 1px solid transparent;
}}
QComboBox {{
    {DROPDOWN_STYLE}
}}
QComboBox QAbstractItemView {{
    {DROPDOWN_STYLE}
}}
QWidget#menu {{
    background-color:transparent;
}}
QWidget#commandAdd {{
    background-color:transparent;
}}
"""
