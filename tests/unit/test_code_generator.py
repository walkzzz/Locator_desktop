#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeGenerator类的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from unittest.mock import Mock, patch
from core.code_generator import CodeGenerator
from core.element import Element


def test_code_generator_creation():
    """测试代码生成器的创建"""
    generator = CodeGenerator()
    assert generator is not None


def test_generate_pywinauto_code():
    """测试生成pywinauto代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    element.name = "确定"
    element.class_name = "Button"
    element.element_type = "Button"
    
    # 生成代码
    code = generator.generate_pywinauto_code(element)
    
    # 验证代码内容
    assert "from pywinauto.application import Application" in code
    assert "app = Application(backend='uia').connect(process=1234)" in code
    assert "window = app.window(handle=5678)" in code
    assert "element = window.child_window(auto_id='button_ok', name='确定', class_name='Button')" in code
    assert "# 操作示例" in code
    assert "element.click()" in code


def test_generate_uiautomation_code():
    """测试生成uiautomation代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    element.name = "确定"
    element.class_name = "Button"
    element.element_type = "Button"
    
    # 生成代码
    code = generator.generate_uiautomation_code(element)
    
    # 验证代码内容
    assert "import uiautomation as auto" in code
    assert "element = " in code
    assert "# 操作示例" in code
    assert "element.Click()" in code


def test_generate_pyautogui_code():
    """测试生成pyautogui代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    element.element_type = "Button"
    
    # 生成代码
    code = generator.generate_pyautogui_code(element)
    
    # 验证代码内容
    assert "import pyautogui" in code
    assert "x = {element.x}" in code
    assert "y = {element.y}" in code
    assert "width = {element.width}" in code
    assert "height = {element.height}" in code
    assert "center_x = x + width // 2" in code
    assert "center_y = y + height // 2" in code
    assert "# 操作示例" in code
    assert "pyautogui.click(center_x, center_y)" in code


def test_generate_win32gui_code():
    """测试生成win32gui代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    element.element_type = "Button"
    
    # 生成代码
    code = generator.generate_win32gui_code(element)
    
    # 验证代码内容
    assert "import win32gui" in code
    assert "import win32api" in code
    assert "import win32con" in code
    assert "element_rect = ({element.x}, {element.y}, {element.x + element.width}, {element.y + element.height})" in code
    assert "hwnd = win32gui.WindowFromPoint((element.x, element.y))" in code
    assert "center_x = element.x + element.width // 2" in code
    assert "center_y = element.y + element.height // 2" in code
    assert "# 操作示例" in code


def test_generate_coordinate_code():
    """测试生成坐标定位代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    
    # 生成代码
    code = generator.generate_coordinate_code(element)
    
    # 验证代码内容
    assert "import win32api" in code
    assert "import win32con" in code
    assert "x = 100" in code
    assert "y = 200" in code
    assert "width = 50" in code
    assert "height = 30" in code
    assert "center_x = x + width // 2" in code
    assert "center_y = y + height // 2" in code
    assert "win32api.SetCursorPos((center_x, center_y))" in code
    assert "win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)" in code


def test_generate_image_recognition_code():
    """测试生成图像识别代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    
    # 生成代码
    code = generator.generate_image_recognition_code(element)
    
    # 验证代码内容
    assert "import cv2" in code
    assert "import numpy as np" in code
    assert "from PIL import ImageGrab" in code
    assert "# 读取模板图像" in code
    assert "template_path = 'element_template.png'" in code
    assert "# 获取屏幕截图" in code
    assert "# 模板匹配" in code
    assert "# 设置匹配阈值" in code
    assert "if max_val >= threshold:" in code
    assert "win32api.SetCursorPos((center_x, center_y))" in code


def test_generate_code_by_method_unknown():
    """测试根据未知方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    element.name = "确定"
    element.class_name = "Button"
    element.element_type = "Button"
    
    # 测试未知方法
    unknown_code = generator.generate_code_by_method(element, method='unknown')
    
    # 验证结果
    assert "# 不支持的定位方法" in unknown_code


def test_generate_code_by_method():
    """测试根据方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    element.name = "确定"
    element.class_name = "Button"
    element.element_type = "Button"
    
    # 测试不同方法
    auto_code = generator.generate_code_by_method(element, method='auto')
    attribute_code = generator.generate_code_by_method(element, method='attribute')
    image_code = generator.generate_code_by_method(element, method='image')
    coordinate_code = generator.generate_code_by_method(element, method='coordinate')
    pyautogui_code = generator.generate_code_by_method(element, method='pyautogui')
    win32gui_code = generator.generate_code_by_method(element, method='win32gui')
    
    # 验证代码类型
    assert "pywinauto" in auto_code
    assert "pywinauto" in attribute_code
    assert "cv2" in image_code
    assert "win32api" in coordinate_code
    assert "pyautogui" in pyautogui_code
    assert "win32gui" in win32gui_code
