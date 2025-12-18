#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ElementCapture类的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from unittest.mock import Mock, patch
from core.element_capture import ElementCapture
from core.element import Element


def test_element_capture_creation():
    """测试元素捕获类的创建"""
    capture = ElementCapture()
    assert capture is not None
    assert capture.capturing is False
    assert capture.last_captured_element is None


def test_test_element_location_success():
    """测试元素定位测试成功情况"""
    capture = ElementCapture()
    
    # 创建一个模拟元素
    element = Element()
    element.window_handle = 1234
    element.automation_id = "test_element"
    
    # 使用mock模拟uiautomation的FromHandle和FindFirst方法
    with patch('core.element_capture.AutomationElement') as mock_automation:
        # 设置mock返回值
        mock_window = Mock()
        mock_element = Mock()
        mock_automation.FromHandle.return_value = mock_window
        mock_window.FindFirst.return_value = mock_element
        
        # 测试定位
        result = capture.test_element_location(element)
        
        # 验证结果
        assert result is True
        mock_automation.FromHandle.assert_called_once_with(1234)
        mock_window.FindFirst.assert_called_once()


def test_test_element_location_failure():
    """测试元素定位测试失败情况"""
    capture = ElementCapture()
    
    # 创建一个模拟元素
    element = Element()
    element.window_handle = 1234
    element.automation_id = "test_element"
    
    # 使用mock模拟uiautomation的FromHandle方法返回None
    with patch('core.element_capture.AutomationElement') as mock_automation:
        mock_automation.FromHandle.return_value = None
        
        # 测试定位
        result = capture.test_element_location(element)
        
        # 验证结果
        assert result is False


def test_test_element_location_no_window_handle():
    """测试没有窗口句柄的元素定位测试"""
    capture = ElementCapture()
    
    # 创建一个没有窗口句柄的元素
    element = Element()
    element.automation_id = "test_element"
    
    # 测试定位
    result = capture.test_element_location(element)
    
    # 验证结果
    assert result is False


def test_test_element_location_no_automation_id():
    """测试没有automation_id的元素定位测试"""
    capture = ElementCapture()
    
    # 创建一个没有automation_id的元素
    element = Element()
    element.window_handle = 1234
    element.name = "测试元素"
    
    # 使用mock模拟uiautomation的FromHandle和FindFirst方法
    with patch('core.element_capture.AutomationElement') as mock_automation:
        # 设置mock返回值
        mock_window = Mock()
        mock_element = Mock()
        mock_automation.FromHandle.return_value = mock_window
        mock_window.FindFirst.return_value = mock_element
        
        # 测试定位
        result = capture.test_element_location(element)
        
        # 验证结果
        assert result is True

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
@patch('core.element_capture.pywinauto')
@patch('core.element_capture.AutomationElement')
def test_get_element_by_coordinate(mock_automation, mock_pywinauto, mock_win32gui, mock_win32api):
    """测试根据坐标获取元素"""
    capture = ElementCapture()
    
    # 设置mock返回值
    mock_automation_element = Mock()
    mock_automation.FromPoint.return_value = mock_automation_element
    
    # 调用方法
    element = capture._get_element_by_coordinate(1234, 100, 200)
    
    # 验证调用
    mock_automation.FromPoint.assert_called_once_with((100, 200))

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
@patch('core.element_capture.pywinauto')
@patch('core.element_capture.AutomationElement')
def test_get_element_by_coordinate_no_automation(mock_automation, mock_pywinauto, mock_win32gui, mock_win32api):
    """测试根据坐标获取元素，当uiautomation获取失败时"""
    capture = ElementCapture()
    
    # 设置mock返回值 - uiautomation获取失败
    mock_automation.FromPoint.side_effect = Exception("uiautomation获取失败")
    
    # 设置pywinauto mock
    mock_app = Mock()
    mock_window = Mock()
    mock_element = Mock()
    mock_pywinauto.Application.return_value = mock_app
    mock_app.connect.return_value = mock_app
    mock_app.window.return_value = mock_window
    mock_window.from_point.return_value = mock_element
    
    # 设置元素信息
    mock_element.element_info = Mock()
    mock_element.element_info.control_type = "Button"
    mock_element.element_info.name = "测试按钮"
    mock_element.element_info.class_name = "Button"
    mock_element.element_info.automation_id = "button_test"
    mock_element.element_info.rectangle = Mock()
    mock_element.element_info.rectangle.left = 100
    mock_element.element_info.rectangle.top = 200
    mock_element.element_info.rectangle.width.return_value = 50
    mock_element.element_info.rectangle.height.return_value = 30
    mock_element.element_info.process_id = 1234
    mock_element.element_info.handle = 5678
    mock_element.is_enabled.return_value = True
    mock_element.is_visible.return_value = True
    
    # 调用方法
    element = capture._get_element_by_coordinate(1234, 100, 200)
    
    # 验证结果
    assert element is not None
    assert element.element_type == "Button"
    assert element.name == "测试按钮"


def test_convert_to_element():
    """测试转换uiautomation元素到自定义Element对象"""
    capture = ElementCapture()
    
    # 创建一个mock的automation元素
    mock_automation_element = Mock()
    mock_automation_element.ControlTypeName = "Button"
    mock_automation_element.ControlType = 50000  # Button的ControlType值
    mock_automation_element.ClassName = "Button"
    mock_automation_element.AutomationId = "button_test"
    mock_automation_element.Name = "测试按钮"
    mock_automation_element.IsEnabled = True
    mock_automation_element.IsOffscreen = False
    mock_automation_element.ProcessId = 1234
    mock_automation_element.NativeWindowHandle = 5678
    
    # 设置BoundingRectangle
    mock_rect = Mock()
    mock_rect.left = 100
    mock_rect.top = 200
    mock_rect.right = 150
    mock_rect.bottom = 230
    mock_automation_element.BoundingRectangle = mock_rect
    
    # 转换元素
    element = capture._convert_to_element(mock_automation_element)
    
    # 验证转换结果
    assert element is not None
    assert isinstance(element, Element)
    assert element.element_type == "Button"
    assert element.automation_id == "button_test"
    assert element.name == "测试按钮"
    assert element.is_enabled is True
    assert element.is_visible is True
    assert element.x == 100
    assert element.y == 200
    assert element.width == 50
    assert element.height == 30
    assert element.process_id == 1234
    assert element.window_handle == 5678