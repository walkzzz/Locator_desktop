#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ElementAnalyzer类的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from unittest.mock import Mock, patch
from core.element_analyzer import ElementAnalyzer
from core.element import Element


def test_element_analyzer_creation():
    """测试ElementAnalyzer实例创建"""
    analyzer = ElementAnalyzer()
    assert analyzer is not None
    assert analyzer.max_depth == 10


def test_get_element_path():
    """测试获取元素路径"""
    analyzer = ElementAnalyzer()
    
    # 创建元素层次结构
    root = Element()
    root.element_type = "Window"
    root.automation_id = "root_window"
    
    parent = Element()
    parent.element_type = "Group"
    parent.name = "容器"
    
    child = Element()
    child.element_type = "Button"
    child.automation_id = "button_ok"
    
    # 构建层次关系
    root.add_child(parent)
    parent.add_child(child)
    
    # 获取元素路径
    path = analyzer.get_element_path(child)
    
    # 验证结果
    assert isinstance(path, str)
    assert "Window" in path
    assert "Group" in path
    assert "Button" in path
    assert "automation_id=\"root_window\"" in path
    assert "automation_id=\"button_ok\"" in path


def test_get_element_unique_identifier():
    """测试获取元素唯一标识符"""
    analyzer = ElementAnalyzer()
    
    # 测试使用automation_id的情况
    element1 = Element()
    element1.automation_id = "unique_id_123"
    element1.element_type = "Button"
    
    identifier1 = analyzer.get_element_unique_identifier(element1)
    assert identifier1 == "automation_id='unique_id_123'"
    
    # 测试使用name和control_type的情况
    element2 = Element()
    element2.name = "确定"
    element2.element_type = "Button"
    
    identifier2 = analyzer.get_element_unique_identifier(element2)
    assert identifier2 == "name='确定' and control_type='Button'"
    
    # 测试使用class_name和control_type的情况
    element3 = Element()
    element3.class_name = "Button"
    element3.element_type = "Button"
    
    identifier3 = analyzer.get_element_unique_identifier(element3)
    assert identifier3 == "class_name='Button' and control_type='Button'"
    
    # 测试使用位置信息的情况
    element4 = Element()
    element4.element_type = "Button"
    element4.x = 100
    element4.y = 200
    
    identifier4 = analyzer.get_element_unique_identifier(element4)
    assert identifier4 == "position=(100, 200)"


def test_analyze_element_compatibility():
    """测试分析元素兼容性"""
    analyzer = ElementAnalyzer()
    
    # 测试完整元素的兼容性
    complete_element = Element()
    complete_element.automation_id = "unique_id"
    complete_element.element_type = "Button"
    complete_element.is_visible = True
    complete_element.is_enabled = True
    
    compatibility = analyzer.analyze_element_compatibility(complete_element)
    
    # 验证结果
    assert isinstance(compatibility, dict)
    assert "pywinauto_support" in compatibility
    assert "uiautomation_support" in compatibility
    assert "recommended_method" in compatibility
    assert "issues" in compatibility
    
    assert compatibility["pywinauto_support"] is True
    assert compatibility["uiautomation_support"] is True
    assert compatibility["recommended_method"] == "attribute"
    assert len(compatibility["issues"]) == 0


def test_analyze_element_compatibility_missing_attr():
    """测试分析缺少属性的元素兼容性"""
    analyzer = ElementAnalyzer()
    
    # 测试缺少唯一标识符的元素
    incomplete_element = Element()
    incomplete_element.element_type = "Button"
    incomplete_element.is_visible = True
    incomplete_element.is_enabled = True
    
    compatibility = analyzer.analyze_element_compatibility(incomplete_element)
    
    # 验证结果
    assert len(compatibility["issues"]) > 0
    assert compatibility["recommended_method"] == "attribute"  # Button类型元素推荐使用attribute方法


def test_analyze_element_compatibility_invisible():
    """测试分析不可见元素的兼容性"""
    analyzer = ElementAnalyzer()
    
    # 测试不可见元素
    invisible_element = Element()
    invisible_element.automation_id = "unique_id"
    invisible_element.element_type = "Button"
    invisible_element.is_visible = False
    invisible_element.is_enabled = True
    
    compatibility = analyzer.analyze_element_compatibility(invisible_element)
    
    # 验证结果
    assert len(compatibility["issues"]) > 0
    assert any("不可见" in issue for issue in compatibility["issues"])


def test_analyze_element_compatibility_disabled():
    """测试分析不可用元素的兼容性"""
    analyzer = ElementAnalyzer()
    
    # 测试不可用元素
    disabled_element = Element()
    disabled_element.automation_id = "unique_id"
    disabled_element.element_type = "Button"
    disabled_element.is_visible = True
    disabled_element.is_enabled = False
    
    compatibility = analyzer.analyze_element_compatibility(disabled_element)
    
    # 验证结果
    assert len(compatibility["issues"]) > 0
    assert any("不可用" in issue for issue in compatibility["issues"])

@patch('core.element_analyzer.pywinauto')
def test_analyze_window(mock_pywinauto):
    """测试分析窗口"""
    analyzer = ElementAnalyzer()
    
    # 创建模拟窗口对象
    mock_window = Mock()
    mock_window.hwnd = 12345
    
    # 模拟pywinauto连接和元素获取
    mock_app = Mock()
    mock_window_element = Mock()
    mock_element_info = Mock()
    
    # 设置模拟属性（注意：width和height应该是属性而不是方法）
    mock_element_info.control_type = "Window"
    mock_element_info.class_name = "TestWindow"
    mock_element_info.automation_id = "test_window"
    mock_element_info.name = "测试窗口"
    
    # 模拟rectangle对象，width和height是属性
    mock_rect = Mock()
    mock_rect.left = 0
    mock_rect.top = 0
    mock_rect.width = 800  # 注意：这是属性，不是方法
    mock_rect.height = 600  # 注意：这是属性，不是方法
    mock_element_info.rectangle = mock_rect
    
    mock_element_info.is_enabled = True
    mock_element_info.is_visible = True
    mock_element_info.process_id = 1234
    mock_element_info.handle = 12345
    
    mock_window_element.element_info = mock_element_info
    mock_window_element.children.return_value = []
    mock_app.window.return_value = mock_window_element
    mock_pywinauto.Application.return_value.connect.return_value = mock_app
    
    # 模拟_convert_pywinauto_to_element返回一个元素对象
    with patch.object(analyzer, '_convert_pywinauto_to_element') as mock_convert:
        mock_root_element = Element()
        mock_root_element.element_type = "Window"
        mock_root_element.class_name = "TestWindow"
        mock_root_element.automation_id = "test_window"
        mock_root_element.name = "测试窗口"
        mock_convert.return_value = mock_root_element
        
        # 模拟_analyze_element_children方法
        with patch.object(analyzer, '_analyze_element_children') as mock_analyze_children:
            # 分析窗口
            root_element = analyzer.analyze_window(mock_window)
            
            # 验证结果
            assert root_element is not None
            assert root_element == mock_root_element
            assert mock_convert.called
            assert mock_analyze_children.called

@patch('builtins.hasattr')
def test_analyze_window_invalid(mock_hasattr):
    """测试分析无效窗口"""
    analyzer = ElementAnalyzer()
    
    # 创建无效窗口对象
    invalid_window = Mock()
    
    # 模拟hasattr返回False，表明窗口没有hwnd属性
    mock_hasattr.return_value = False
    
    # 分析窗口
    root_element = analyzer.analyze_window(invalid_window)
    
    # 验证结果
    assert root_element is None


def test_build_path_part():
    """测试构建路径部分"""
    analyzer = ElementAnalyzer()
    
    # 测试使用automation_id的情况
    element1 = Element()
    element1.element_type = "Button"
    element1.automation_id = "button_ok"
    element1.depth = 1
    
    # 访问私有方法
    path_part1 = analyzer._build_path_part(element1)
    assert path_part1 == '<Button automation_id="button_ok" depth=1>'
    
    # 测试使用name的情况
    element2 = Element()
    element2.element_type = "Group"
    element2.name = "容器"
    element2.depth = 2
    
    path_part2 = analyzer._build_path_part(element2)
    assert path_part2 == '<Group name="容器" depth=2>'
    
    # 测试使用class_name的情况
    element3 = Element()
    element3.element_type = "Edit"
    element3.class_name = "Edit"
    element3.depth = 3
    
    path_part3 = analyzer._build_path_part(element3)
    assert path_part3 == '<Edit class_name="Edit" depth=3>'
    
    # 测试使用默认属性的情况
    element4 = Element()
    element4.element_type = "Custom"
    element4.depth = 4
    
    path_part4 = analyzer._build_path_part(element4)
    assert path_part4 == '<Custom depth=4>'