# -*- coding: utf-8 -*-
"""
Locator_desktop核心模块
"""

from .element import Element
from .element_capture import ElementCapture
from .element_analyzer import ElementAnalyzer
from .code_generator import CodeGenerator
from .locator_strategy import LocatorStrategy, LocatorMethod, locator_strategy
from .stability_analyzer import StabilityAnalyzer, stability_analyzer

__all__ = [
    # 核心类
    'Element',
    'ElementCapture',
    'ElementAnalyzer',
    'CodeGenerator',
    'LocatorStrategy',
    'StabilityAnalyzer',
    
    # 枚举类
    'LocatorMethod',
    
    # 全局实例
    'locator_strategy',
    'stability_analyzer'
]
