# -*- coding: utf-8 -*-
"""
Locator_desktop核心模块
"""

from .element import Element
from .element_capture import ElementCapture
from .element_analyzer import ElementAnalyzer
from .code_generator import CodeGenerator

__all__ = [
    'Element',
    'ElementCapture',
    'ElementAnalyzer',
    'CodeGenerator'
]
