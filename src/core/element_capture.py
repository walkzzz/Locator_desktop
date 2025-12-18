#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import win32gui
import win32con
import win32api
import pywinauto
import uiautomation as auto

from .element import Element


class ElementCapture:
    """元素捕获核心逻辑类"""

    def __init__(self):
        self.capturing = False
        self.last_captured_element = None
    
    def capture_element(self):
        """捕获元素
        
        Returns:
            捕获到的元素对象，没有捕获到返回None
        """
        print("开始捕获元素，请将鼠标移动到目标元素上，按下Ctrl键确认...")
        
        self.capturing = True
        captured_element = None
        
        try:
            # 等待用户按下Ctrl键
            while self.capturing:
                # 获取当前鼠标位置
                x, y = win32api.GetCursorPos()
                
                # 获取鼠标下的窗口
                hwnd = win32gui.WindowFromPoint((x, y))
                if hwnd:
                    # 使用pywinauto获取元素
                    element = self._get_element_by_coordinate(hwnd, x, y)
                    if element:
                        self.last_captured_element = element
                        print(f"捕获到元素: {element}")
                
                # 检查是否按下了Ctrl键
                if win32api.GetKeyState(win32con.VK_CONTROL) < 0:
                    captured_element = self.last_captured_element
                    break
                
                # 短暂延迟，减少CPU占用
                time.sleep(0.1)
        except Exception as e:
            print(f"捕获元素时发生错误: {e}")
        finally:
            self.capturing = False
        
        return captured_element
    
    def _get_element_by_coordinate(self, hwnd, x, y):
        """根据坐标获取元素
        
        Args:
            hwnd: 窗口句柄
            x: 鼠标x坐标
            y: 鼠标y坐标
            
        Returns:
            元素对象，获取失败返回None
        """
        try:
            # 使用pywinauto获取元素
            app = pywinauto.Application(backend='uia').connect(handle=hwnd)
            window = app.window(handle=hwnd)
            element = window.from_point((x, y))
            if element:
                return self._convert_pywinauto_to_element(element)
        except Exception as e:
            print(f"使用pywinauto获取元素失败: {e}")
        
        return None
    
    def _convert_to_element(self, automation_element):
        """将uiautomation元素转换为自定义Element对象
        
        Args:
            automation_element: uiautomation元素对象
            
        Returns:
            自定义Element对象
        """
        element = Element()
        
        # 基本信息
        element.element_type = automation_element.ControlTypeName
        element.control_type = automation_element.ControlType
        element.class_name = automation_element.ClassName
        element.automation_id = automation_element.AutomationId
        
        # 元素名称和文本
        element.name = automation_element.Name
        element.text = automation_element.Name
        
        # 元素位置和尺寸
        rect = automation_element.BoundingRectangle
        element.x = rect.left
        element.y = rect.top
        element.width = rect.right - rect.left
        element.height = rect.bottom - rect.top
        
        # 元素状态
        element.is_enabled = automation_element.IsEnabled
        element.is_visible = automation_element.IsOffscreen == False
        
        # 其他属性
        element.process_id = automation_element.ProcessId
        element.window_handle = automation_element.NativeWindowHandle
        
        return element
    
    def _convert_pywinauto_to_element(self, pywinauto_element):
        """将pywinauto元素转换为自定义Element对象
        
        Args:
            pywinauto_element: pywinauto元素对象
            
        Returns:
            自定义Element对象
        """
        element = Element()
        
        # 基本信息
        element.element_type = pywinauto_element.element_info.control_type
        element.control_type = pywinauto_element.element_info.control_type
        element.class_name = pywinauto_element.element_info.class_name
        element.automation_id = pywinauto_element.element_info.automation_id
        
        # 元素名称和文本
        element.name = pywinauto_element.element_info.name
        element.text = pywinauto_element.element_info.name
        
        # 元素位置和尺寸
        rect = pywinauto_element.element_info.rectangle
        element.x = rect.left
        element.y = rect.top
        element.width = rect.width()
        element.height = rect.height()
        
        # 元素状态
        element.is_enabled = pywinauto_element.is_enabled()
        element.is_visible = pywinauto_element.is_visible()
        
        # 其他属性
        element.process_id = pywinauto_element.element_info.process_id
        element.window_handle = pywinauto_element.element_info.handle
        
        return element
    
    def test_element_location(self, element):
        """测试元素定位是否有效
        
        Args:
            element: 元素对象
            
        Returns:
            定位是否成功
        """
        try:
            if not element or not element.window_handle:
                return False
            
            # 使用pywinauto测试定位
            app = pywinauto.Application(backend='uia').connect(handle=element.window_handle)
            window = app.window(handle=element.window_handle)
            
            # 根据automation_id查找
            if element.automation_id:
                try:
                    found_element = window.child_window(auto_id=element.automation_id)
                    if found_element.exists():
                        return True
                except Exception as e:
                    print(f"根据automation_id查找失败: {e}")
            
            # 根据名称查找
            if element.name:
                try:
                    found_element = window.child_window(name=element.name)
                    if found_element.exists():
                        return True
                except Exception as e:
                    print(f"根据名称查找失败: {e}")
            
            return False
        except Exception as e:
            print(f"测试元素定位失败: {e}")
            return False
    
    def capture_element_by_image(self, image_path, confidence=0.8):
        """通过图像识别捕获元素
        
        Args:
            image_path: 图像文件路径
            confidence: 识别置信度
            
        Returns:
            元素对象，识别失败返回None
        """
        try:
            import cv2
            import numpy as np
            from PIL import ImageGrab
            
            # 读取模板图像
            template = cv2.imread(image_path)
            if template is None:
                print("无法读取模板图像")
                return None
            
            # 获取屏幕截图
            screenshot = ImageGrab.grab()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                # 创建元素对象
                element = Element()
                element.element_type = "ImageMatched"
                element.x = max_loc[0]
                element.y = max_loc[1]
                element.width = template.shape[1]
                element.height = template.shape[0]
                element.name = f"ImageMatched_{max_val:.2f}"
                
                return element
            else:
                print(f"图像匹配置信度不足: {max_val:.2f} < {confidence}")
                return None
        except Exception as e:
            print(f"图像识别捕获元素失败: {e}")
            return None
