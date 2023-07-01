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
BACKGROUND_STYLE = 'background-color: #36454F'
MENU_BACKGROUND_STYLE = """
text-align: left;
background-color:transparent;
"""

LINE_EDIT_STYLE = f"""
background-color:{TEXT_BACKGROUND_COLOR};
border-radius:2px;
color: white;
"""

LINE_EDIT_ERROR_STYLE = LINE_EDIT_STYLE + "\nborder: 2px solid red"

BUTTON_STYLE = f"""
QPushButton {{
    background-color:transparent;
    font:bold 12px;
    color: {FONT_COLOR};
}}
QPushButton:hover {{
    font:bold 13px;
    color: white;
}}
"""

DROPDOWN_STYLE = f"""
background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
color: white;
font:bold 10px;
"""

DISPLAY_STYLE = f"""
color:white;
font:bold 10px;
background-color:{TEXT_BACKGROUND_COLOR};
"""
