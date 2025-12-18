#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinauto

from .element import Element


class ElementAnalyzer:
    """元素分析器类，负责分析窗口的UI元素结构"""

    def __init__(self):
        self.max_depth = 10  # 最大分析深度
    
    def analyze_window(self, window):
        """分析窗口的UI元素结构
        
        Args:
            window: 窗口对象，包含hwnd属性
            
        Returns:
            根元素对象，分析失败返回None
        """
        if not hasattr(window, 'hwnd'):
            print("无效的窗口对象")
            return None
        
        try:
            # 使用pywinauto分析窗口
            window_handle = window.hwnd
            app = pywinauto.Application(backend='uia').connect(handle=window_handle)
            window_element = app.window(handle=window_handle)
            
            # 转换为自定义Element对象
            root_element = self._convert_pywinauto_to_element(window_element.element_info)
            
            # 递归分析子元素
            self._analyze_element_children(window_element, root_element, 1)
            
            return root_element
        except Exception as e:
            print(f"分析窗口元素失败: {e}")
            return None
    
    def _analyze_element_children(self, parent_pywinauto_element, parent_element, current_depth):
        """递归分析元素的子元素
        
        Args:
            parent_pywinauto_element: 父pywinauto元素
            parent_element: 父自定义元素
            current_depth: 当前深度
        """
        if current_depth > self.max_depth:
            return
        
        try:
            # 获取子元素
            children_pywinauto_elements = parent_pywinauto_element.children()
            
            for child_pywinauto_element in children_pywinauto_elements:
                # 转换为自定义Element对象
                child_element = self._convert_pywinauto_to_element(child_pywinauto_element.element_info)
                child_element.depth = current_depth
                
                # 添加到父元素
                parent_element.add_child(child_element)
                
                # 递归分析子元素
                self._analyze_element_children(child_pywinauto_element, child_element, current_depth + 1)
        except Exception as e:
            print(f"分析子元素失败: {e}")
    
    def _convert_pywinauto_to_element(self, pywinauto_element_info):
        """将pywinauto元素信息转换为自定义Element对象
        
        Args:
            pywinauto_element_info: pywinauto元素信息对象
            
        Returns:
            自定义Element对象
        """
        element = Element()
        
        # 基本信息
        element.element_type = pywinauto_element_info.control_type
        element.control_type = pywinauto_element_info.control_type
        element.class_name = pywinauto_element_info.class_name
        element.automation_id = pywinauto_element_info.automation_id
        
        # 元素名称和文本
        element.name = pywinauto_element_info.name
        element.text = pywinauto_element_info.name
        
        # 元素位置和尺寸
        rect = pywinauto_element_info.rectangle
        element.x = rect.left
        element.y = rect.top
        element.width = rect.width()
        element.height = rect.height()
        
        # 元素状态
        element.is_enabled = pywinauto_element_info.is_enabled
        element.is_visible = pywinauto_element_info.is_visible
        
        # 其他属性
        element.process_id = pywinauto_element_info.process_id
        element.window_handle = pywinauto_element_info.handle
        
        return element
    
    def get_element_path(self, element):
        """获取元素的定位路径
        
        Args:
            element: 元素对象
            
        Returns:
            元素定位路径字符串
        """
        if not element:
            return ""
        
        path_parts = []
        current = element
        
        while current:
            # 构建路径部分
            path_part = self._build_path_part(current)
            path_parts.append(path_part)
            current = current.parent
        
        # 反转路径，从根到当前元素
        path_parts.reverse()
        
        return "\\n".join(path_parts)
    
    def _build_path_part(self, element):
        """构建路径的一部分
        
        Args:
            element: 元素对象
            
        Returns:
            路径部分字符串
        """
        # 根据元素属性构建唯一标识
        if element.automation_id:
            return f"<{element.element_type} automation_id=\"{element.automation_id}\" depth={element.depth}>"
        elif element.name:
            return f"<{element.element_type} name=\"{element.name}\" depth={element.depth}>"
        elif element.class_name:
            return f"<{element.element_type} class_name=\"{element.class_name}\" depth={element.depth}>"
        else:
            return f"<{element.element_type} depth={element.depth}>"
    
    def analyze_element_compatibility(self, element):
        """分析元素的兼容性
        
        Args:
            element: 元素对象
            
        Returns:
            兼容性分析结果
        """
        compatibility = {
            'pywinauto_support': True,
            'uiautomation_support': True,
            'recommended_method': 'auto',
            'issues': []
        }
        
        # 检查元素属性完整性
        if not element.automation_id and not element.name and not element.class_name:
            compatibility['issues'].append('元素缺少唯一标识属性，可能导致定位不稳定')
            compatibility['recommended_method'] = 'image'
        
        # 检查元素可见性
        if not element.is_visible:
            compatibility['issues'].append('元素当前不可见，可能导致定位失败')
        
        # 检查元素可用性
        if not element.is_enabled:
            compatibility['issues'].append('元素当前不可用')
        
        # 根据元素类型推荐定位方式
        if element.element_type in ['Button', 'Edit', 'ComboBox', 'List', 'CheckBox', 'RadioButton']:
            compatibility['recommended_method'] = 'attribute'
        elif element.element_type in ['Image', 'Custom']:
            compatibility['recommended_method'] = 'image'
        
        return compatibility
    
    def get_element_unique_identifier(self, element):
        """获取元素的唯一标识符
        
        Args:
            element: 元素对象
            
        Returns:
            唯一标识符字符串
        """
        # 优先使用automation_id
        if element.automation_id:
            return f"automation_id='{element.automation_id}'"
        
        # 其次使用名称和类型组合
        if element.name and element.element_type:
            return f"name='{element.name}' and control_type='{element.element_type}'"
        
        # 再次使用类名和类型组合
        if element.class_name and element.element_type:
            return f"class_name='{element.class_name}' and control_type='{element.element_type}'"
        
        # 最后使用位置信息
        return f"position=({element.x}, {element.y})"
