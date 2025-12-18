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
    """测试ElementCapture实例创建"""
    capture = ElementCapture()
    assert capture is not None
    assert capture.capturing is False
    assert capture.last_captured_element is None

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_capture_element(mock_win32gui, mock_win32api):
    """测试捕获元素"""
    capture = ElementCapture()
    
    # 模拟鼠标位置和窗口句柄
    mock_win32api.GetCursorPos.return_value = (100, 200)
    mock_win32gui.WindowFromPoint.return_value = 1234
    
    # 模拟Ctrl键未按下，然后按下
    mock_win32api.GetKeyState.side_effect = [0, 0, -1]  # 先返回0，最后返回-1表示按下
    
    # 模拟_get_element_by_coordinate返回元素
    mock_element = Element()
    mock_element.name = "测试按钮"
    
    # 使用patch模拟内部方法
    with patch.object(capture, '_get_element_by_coordinate', return_value=mock_element) as mock_get_element:
        # 捕获元素
        captured_element = capture.capture_element()
        
        # 验证结果
        assert captured_element is not None
        assert captured_element == mock_element
        assert mock_get_element.called
        assert capture.last_captured_element == mock_element

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_capture_element_no_element(mock_win32gui, mock_win32api):
    """测试未捕获到元素的情况"""
    capture = ElementCapture()
    
    # 模拟鼠标位置和窗口句柄
    mock_win32api.GetCursorPos.return_value = (100, 200)
    mock_win32gui.WindowFromPoint.return_value = 1234
    
    # 模拟Ctrl键按下
    mock_win32api.GetKeyState.return_value = -1
    
    # 模拟_get_element_by_coordinate返回None
    with patch.object(capture, '_get_element_by_coordinate', return_value=None) as mock_get_element:
        # 捕获元素
        captured_element = capture.capture_element()
        
        # 验证结果
        assert captured_element is None

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_capture_element_exception(mock_win32gui, mock_win32api):
    """测试捕获元素时发生异常"""
    capture = ElementCapture()
    
    # 模拟鼠标位置和窗口句柄
    mock_win32api.GetCursorPos.return_value = (100, 200)
    mock_win32gui.WindowFromPoint.return_value = 1234
    
    # 模拟Ctrl键按下
    mock_win32api.GetKeyState.return_value = -1
    
    # 模拟_get_element_by_coordinate抛出异常
    with patch.object(capture, '_get_element_by_coordinate', side_effect=Exception("Test exception")) as mock_get_element:
        # 捕获元素
        captured_element = capture.capture_element()
        
        # 验证结果
        assert captured_element is None
        assert capture.capturing is False

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_test_element_location(mock_win32gui, mock_win32api):
    """测试元素定位测试"""
    capture = ElementCapture()
    
    # 创建测试元素
    element = Element()
    element.window_handle = 1234
    element.automation_id = "button_ok"
    element.name = "确定"
    
    # 模拟_detect_application_type返回WPF
    with patch.object(capture, '_detect_application_type', return_value='WPF'):
        # 模拟pywinauto应用连接和元素查找
        with patch('core.element_capture.pywinauto') as mock_pywinauto:
            # 设置模拟对象
            mock_app = Mock()
            mock_window = Mock()
            mock_element = Mock()
            
            mock_element.exists.return_value = True
            mock_window.child_window.return_value = mock_element
            mock_app.window.return_value = mock_window
            mock_pywinauto.Application.return_value.connect.return_value = mock_app
            
            # 测试定位
            result = capture.test_element_location(element)
            
            # 验证结果
            assert result is True
            mock_pywinauto.Application.called
            mock_window.child_window.called
            mock_element.exists.called

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_test_element_location_no_automation_id(mock_win32gui, mock_win32api):
    """测试没有automation_id的元素定位测试"""
    capture = ElementCapture()
    
    # 创建一个没有automation_id的元素
    element = Element()
    element.window_handle = 1234
    element.name = "测试元素"
    
    # 模拟_detect_application_type返回WPF
    with patch.object(capture, '_detect_application_type', return_value='WPF'):
        # 模拟pywinauto应用连接和元素查找
        with patch('core.element_capture.pywinauto') as mock_pywinauto:
            # 设置模拟对象
            mock_app = Mock()
            mock_window = Mock()
            mock_element = Mock()
            
            mock_element.exists.return_value = True
            mock_window.child_window.return_value = mock_element
            mock_app.window.return_value = mock_window
            mock_pywinauto.Application.return_value.connect.return_value = mock_app
            
            # 测试定位
            result = capture.test_element_location(element)
            
            # 验证结果
            assert result is True

@patch('core.element_capture.win32api')
@patch('core.element_capture.win32gui')
def test_test_element_location_failure(mock_win32gui, mock_win32api):
    """测试元素定位失败"""
    capture = ElementCapture()
    
    # 创建测试元素
    element = Element()
    element.window_handle = 1234
    element.automation_id = "non_existent_id"
    
    # 模拟_detect_application_type返回WPF
    with patch.object(capture, '_detect_application_type', return_value='WPF'):
        # 模拟pywinauto应用连接，但元素不存在
        with patch('core.element_capture.pywinauto') as mock_pywinauto:
            # 设置模拟对象
            mock_app = Mock()
            mock_window = Mock()
            mock_element = Mock()
            
            mock_element.exists.return_value = False
            mock_window.child_window.return_value = mock_element
            mock_app.window.return_value = mock_window
            mock_pywinauto.Application.return_value.connect.return_value = mock_app
            
            # 测试定位
            result = capture.test_element_location(element)
            
            # 验证结果
            assert result is False

@patch('core.element_capture.win32api')
def test_get_element_by_coordinate(mock_win32api):
    """测试根据坐标获取元素"""
    capture = ElementCapture()
    
    # 模拟窗口句柄和坐标
    hwnd = 1234
    x, y = 100, 200
    
    # 模拟_get_element_by_coordinate_with_backend返回元素
    mock_element = Element()
    mock_element.name = "测试按钮"
    
    # 模拟应用类型检测
    with patch.object(capture, '_detect_application_type', return_value='WPF'):
        with patch.object(capture, '_get_element_by_coordinate_with_backend', return_value=mock_element) as mock_get_by_backend:
            # 获取元素
            element = capture._get_element_by_coordinate(hwnd, x, y)
            
            # 验证结果
            assert element is not None
            assert element == mock_element
            assert mock_get_by_backend.called

@patch('core.element_capture.win32api')
def test_get_element_by_coordinate_with_backend(mock_win32api):
    """测试使用指定backend根据坐标获取元素"""
    capture = ElementCapture()
    
    # 模拟窗口句柄和坐标
    hwnd = 1234
    x, y = 100, 200
    
    # 模拟pywinauto应用连接和元素获取
    mock_element = Element()
    mock_element.name = "测试按钮"
    
    with patch('core.element_capture.pywinauto') as mock_pywinauto:
        # 设置模拟对象
        mock_app = Mock()
        mock_window = Mock()
        mock_pywinauto_element = Mock()
        
        mock_window.from_point.return_value = mock_pywinauto_element
        mock_app.window.return_value = mock_window
        mock_pywinauto.Application.return_value.connect.return_value = mock_app
        
        # 模拟_convert_pywinauto_to_element返回元素
        with patch.object(capture, '_convert_pywinauto_to_element', return_value=mock_element) as mock_convert:
            # 获取元素
            element = capture._get_element_by_coordinate_with_backend(hwnd, x, y, backend='uia')
            
            # 验证结果
            assert element is not None
            assert element == mock_element
            assert mock_convert.called

@patch('core.element_capture.win32api')
def test_get_element_by_coordinate_with_backend_failure(mock_win32api):
    """测试使用指定backend根据坐标获取元素失败"""
    capture = ElementCapture()
    
    # 模拟窗口句柄和坐标
    hwnd = 1234
    x, y = 100, 200
    
    # 模拟pywinauto抛出异常
    with patch('core.element_capture.pywinauto') as mock_pywinauto:
        mock_pywinauto.Application.return_value.connect.return_value = Mock()
        mock_pywinauto.Application.return_value.connect.return_value.window.return_value.from_point.side_effect = Exception("Test exception")
        
        # 获取元素
        element = capture._get_element_by_coordinate_with_backend(hwnd, x, y, backend='uia')
        
        # 验证结果
        assert element is None


def test_detect_application_type():
    """测试检测应用类型"""
    capture = ElementCapture()
    
    # 模拟win32gui.GetClassName返回不同的类名
    with patch('core.element_capture.win32gui') as mock_win32gui:
        # 测试Qt应用
        mock_win32gui.GetClassName.return_value = "Qt5QWindowIcon"
        assert capture._detect_application_type(1234) == "Qt"
        
        # 测试WinForms应用
        mock_win32gui.GetClassName.return_value = "WindowsForms10.Window.8.app.0.33c0d9d"
        assert capture._detect_application_type(1234) == "WinForms"
        
        # 测试WPF应用
        mock_win32gui.GetClassName.return_value = "HwndWrapper[Locator_desktop.exe;;abcdef12-3456-7890-abcd-ef1234567890]"
        assert capture._detect_application_type(1234) == "WPF"
        
        # 测试MFC应用
        mock_win32gui.GetClassName.return_value = "Afx:00400000:b:00010003:00000006:00000000"
        assert capture._detect_application_type(1234) == "MFC"
        
        # 测试未知应用
        mock_win32gui.GetClassName.return_value = "UnknownClass"
        assert capture._detect_application_type(1234) == "Unknown"


def test_convert_pywinauto_to_element():
    """测试将pywinauto元素转换为自定义Element对象"""
    capture = ElementCapture()
    
    # 创建模拟的pywinauto元素
    mock_pywinauto_element = Mock()
    
    # 设置模拟属性
    mock_element_info = Mock()
    mock_element_info.control_type = "Button"
    mock_element_info.class_name = "Button"
    mock_element_info.automation_id = "button_ok"
    mock_element_info.name = "确定"
    
    # 设置矩形
    mock_rect = Mock()
    mock_rect.left = 100
    mock_rect.top = 200
    mock_rect.width.return_value = 50
    mock_rect.height.return_value = 30
    mock_element_info.rectangle = mock_rect
    
    mock_element_info.process_id = 1234
    mock_element_info.handle = 12345
    
    mock_pywinauto_element.element_info = mock_element_info
    mock_pywinauto_element.is_enabled.return_value = True
    mock_pywinauto_element.is_visible.return_value = True
    
    # 转换元素
    element = capture._convert_pywinauto_to_element(mock_pywinauto_element)
    
    # 验证结果
    assert element is not None
    assert element.element_type == "Button"
    assert element.class_name == "Button"
    assert element.automation_id == "button_ok"
    assert element.name == "确定"
    assert element.x == 100
    assert element.y == 200
    assert element.width == 50
    assert element.height == 30
    assert element.is_enabled is True
    assert element.is_visible is True
    assert element.process_id == 1234
    assert element.window_handle == 12345


def test_detect_application_type_exception():
    """测试检测应用类型时发生异常"""
    capture = ElementCapture()
    
    # 模拟win32gui.GetClassName抛出异常
    with patch('core.element_capture.win32gui') as mock_win32gui:
        mock_win32gui.GetClassName.side_effect = Exception("Test exception")
        
        # 检测应用类型
        app_type = capture._detect_application_type(1234)
        
        # 验证结果
        assert app_type == "Unknown"