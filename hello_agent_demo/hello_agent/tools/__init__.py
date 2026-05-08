#!/usr/bin/python3
"""
# -*- coding: utf-8 -*-
# Author: Phoss.Xu
# Email: phosssuki@gmail.com
# CreateDate: 2026/04/14
# Description: 
"""

from .weather import get_weather
from .attraction import get_attraction

available_tools = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

__all__ = ["available_tools"]