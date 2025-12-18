#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Element类的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from core.element import Element


def test_element_creation():
    """测试元素创建"""
    element = Element()
    assert element is not None
    assert element.name is None
    assert element.element_type is None
    assert element.children == []
    assert element.depth == 0
    assert element.parent is None
    assert element.attributes == {}


def test_element_attributes():
    """测试元素属性设置和获取"""
    element = Element()
    
    # 设置属性
    element.name = "测试元素"
    element.element_type = "Button"
    element.automation_id = "button_ok"
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    
    # 验证属性
    assert element.name == "测试元素"
    assert element.element_type == "Button"
    assert element.automation_id == "button_ok"
    assert element.x == 100
    assert element.y == 200
    assert element.width == 50
    assert element.height == 30


def test_add_child():
    """测试添加子元素"""
    parent = Element()
    child = Element()
    
    parent.add_child(child)
    
    # 验证父子关系
    assert len(parent.children) == 1
    assert child in parent.children
    assert child.parent == parent
    assert child.depth == 1


def test_add_multiple_children():
    """测试添加多个子元素"""
    parent = Element()
    
    # 添加3个子元素
    for i in range(3):
        child = Element()
        child.name = f"子元素{i}"
        parent.add_child(child)
    
    # 验证子元素数量
    assert len(parent.children) == 3
    assert all(child.parent == parent for child in parent.children)
    assert all(child.depth == 1 for child in parent.children)


def test_element_path():
    """测试获取元素路径"""
    # 创建元素层次结构
    root = Element()
    root.name = "根元素"
    root.element_type = "Window"
    
    parent = Element()
    parent.name = "父元素"
    parent.element_type = "Group"
    
    child = Element()
    child.name = "子元素"
    child.element_type = "Button"
    
    # 构建层次关系
    root.add_child(parent)
    parent.add_child(child)
    
    # 获取路径
    root_path = root.get_path()
    parent_path = parent.get_path()
    child_path = child.get_path()
    
    # 验证路径
    assert "Window(根元素)" in root_path
    assert "Window(根元素) > Group(父元素)" in parent_path
    assert "Window(根元素) > Group(父元素) > Button(子元素)" in child_path


def test_element_str_representation():
    """测试元素字符串表示"""
    element = Element()
    element.name = "测试按钮"
    element.element_type = "Button"
    element.x = 100
    element.y = 200
    element.width = 50
    element.height = 30
    
    element_str = str(element)
    assert "Button" in element_str
    assert "测试按钮" in element_str
    assert "(100, 200)" in element_str
    assert "[50x30]" in element_str


def test_element_attributes_dict():
    """测试元素自定义属性字典"""
    element = Element()
    
    # 设置自定义属性
    element.attributes["custom_attr1"] = "值1"
    element.attributes["custom_attr2"] = 123
    element.attributes["custom_attr3"] = True
    
    # 验证自定义属性
    assert len(element.attributes) == 3
    assert element.attributes["custom_attr1"] == "值1"
    assert element.attributes["custom_attr2"] == 123
    assert element.attributes["custom_attr3"] is True


def test_element_state_attributes():
    """测试元素状态属性"""
    element = Element()
    
    # 设置状态属性
    element.is_enabled = True
    element.is_visible = True
    element.is_checked = False
    element.text = "按钮文本"
    
    # 验证状态属性
    assert element.is_enabled is True
    assert element.is_visible is True
    assert element.is_checked is False
    assert element.text == "按钮文本"


def test_element_process_and_window():
    """测试元素进程和窗口属性"""
    element = Element()
    
    # 设置进程和窗口属性
    element.process_id = 1234
    element.window_handle = 5678
    
    # 验证属性
    assert element.process_id == 1234
    assert element.window_handle == 5678
