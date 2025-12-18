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
from core.code_generator import CodeGenerator
from core.element import Element


def test_code_generator_creation():
    """测试代码生成器创建"""
    generator = CodeGenerator()
    assert generator is not None


def test_generate_pywinauto_code():
    """测试生成pywinauto代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    element.name = "确定按钮"
    element.element_type = "Button"
    
    # 生成代码
    code = generator.generate_pywinauto_code(element)
    
    # 验证代码包含必要的部分
    assert "from pywinauto.application import Application" in code
    assert "app = Application(backend='uia').connect(process=1234)" in code
    assert "window = app.window(handle=5678)" in code
    assert "element = window.child_window(auto_id='button_ok'" in code
    assert "element.click()" in code


def test_generate_uiautomation_code():
    """测试生成uiautomation代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    element.automation_id = "button_ok"
    element.name = "确定按钮"
    element.element_type = "Button"
    element.depth = 2
    
    # 生成代码
    code = generator.generate_uiautomation_code(element)
    
    # 验证代码包含必要的部分
    assert "import uiautomation as auto" in code
    assert "element = auto.GetRootControl()" in code
    assert "ButtonControl(" in code
    assert "AutomationId='button_ok'" in code
    assert "Depth=2" in code
    assert "element.Click()" in code


def test_generate_coordinate_code():
    """测试生成坐标定位代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    
    # 生成代码
    code = generator.generate_coordinate_code(element)
    
    # 验证代码包含必要的部分
    assert "import win32api" in code
    assert "import win32con" in code
    assert "x = 100" in code
    assert "y = 200" in code
    assert "width = 50" in code
    assert "height = 30" in code
    assert "center_x = x + width // 2" in code
    assert "win32api.SetCursorPos(" in code
    assert "win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN" in code


def test_generate_image_recognition_code():
    """测试生成图像识别定位代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    
    # 生成代码
    code = generator.generate_image_recognition_code(element)
    
    # 验证代码包含必要的部分
    assert "import cv2" in code
    assert "import numpy as np" in code
    assert "from PIL import ImageGrab" in code
    assert "template_path = 'element_template.png'" in code
    assert "template = cv2.imread(template_path)" in code
    assert "result = cv2.matchTemplate(" in code
    assert "max_val, max_loc" in code
    assert "threshold = 0.8" in code


def test_generate_code_by_method_auto():
    """测试根据自动方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个有automation_id的测试元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    
    # 生成代码
    code = generator.generate_code_by_method(element, method="auto")
    
    # 验证生成的是pywinauto代码
    assert "from pywinauto.application import Application" in code


def test_generate_code_by_method_attribute():
    """测试根据属性定位方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.automation_id = "button_ok"
    
    # 生成代码
    code = generator.generate_code_by_method(element, method="attribute")
    
    # 验证生成的是属性定位代码
    assert "from pywinauto.application import Application" in code
    assert "element = window.child_window(" in code


def test_generate_code_by_method_image():
    """测试根据图像识别方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    
    # 生成代码
    code = generator.generate_code_by_method(element, method="image")
    
    # 验证生成的是图像识别代码
    assert "import cv2" in code
    assert "template_path = 'element_template.png'" in code


def test_generate_code_by_method_coordinate():
    """测试根据坐标定位方法生成代码"""
    generator = CodeGenerator()
    
    # 创建一个测试元素
    element = Element()
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    
    # 生成代码
    code = generator.generate_code_by_method(element, method="coordinate")
    
    # 验证生成的是坐标定位代码
    assert "import win32api" in code
    assert "win32api.SetCursorPos(" in code


def test_generate_code_without_automation_id():
    """测试生成没有automation_id的元素代码"""
    generator = CodeGenerator()
    
    # 创建一个没有automation_id的测试元素
    element = Element()
    element.process_id = 1234
    element.window_handle = 5678
    element.name = "确定按钮"
    element.class_name = "Button"
    
    # 生成代码
    code = generator.generate_pywinauto_code(element)
    
    # 验证代码使用name和class_name进行定位
    assert "name='确定按钮'" in code
    assert "class_name='Button'" in code


def test_generate_code_with_different_element_types():
    """测试生成不同元素类型的代码"""
    generator = CodeGenerator()
    
    # 测试按钮元素
    button_element = Element()
    button_element.process_id = 1234
    button_element.window_handle = 5678
    button_element.automation_id = "button_test"
    button_element.element_type = "Button"
    button_code = generator.generate_pywinauto_code(button_element)
    assert "element.click()" in button_code
    
    # 测试输入框元素
    edit_element = Element()
    edit_element.process_id = 1234
    edit_element.window_handle = 5678
    edit_element.automation_id = "edit_test"
    edit_element.element_type = "Edit"
    edit_code = generator.generate_pywinauto_code(edit_element)
    assert "element.set_text('测试文本')" in edit_code
    assert "element.type_keys('{ENTER}')" in edit_code
    
    # 测试复选框元素
    checkbox_element = Element()
    checkbox_element.process_id = 1234
    checkbox_element.window_handle = 5678
    checkbox_element.automation_id = "checkbox_test"
    checkbox_element.element_type = "CheckBox"
    checkbox_code = generator.generate_pywinauto_code(checkbox_element)
    assert "element.toggle()" in checkbox_code


def test_generate_code_without_process_id():
    """测试生成没有进程ID的元素代码"""
    generator = CodeGenerator()
    
    # 创建一个没有进程ID的测试元素
    element = Element()
    element.window_handle = 5678
    element.automation_id = "button_ok"
    
    # 生成代码
    code = generator.generate_pywinauto_code(element)
    
    # 验证代码仍然可以生成
    assert "from pywinauto.application import Application" in code
    assert "app = Application(backend='uia').connect(process=0)" in code
    assert "window = app.window(handle=5678)" in code
