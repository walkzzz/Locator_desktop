#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""自动化依赖适配层，用于封装不同版本依赖库的API差异"""

import uiautomation
import pywinauto


class AutomationAdapter:
    """自动化依赖适配层，提供统一的API接口，隐藏底层库的版本差异"""
    
    @staticmethod
    def get_element_by_id(parent, automation_id):
        """根据Automation ID获取元素，兼容不同版本的uiautomation库
        
        Args:
            parent: 父元素
            automation_id: Automation ID
            
        Returns:
            找到的元素，找不到返回None
        """
        try:
            # 检查uiautomation版本
            if hasattr(uiautomation, '__version__'):
                version_parts = uiautomation.__version__.split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1])
                patch = int(version_parts[2]) if len(version_parts) > 2 else 0
                
                # 根据版本选择不同的API
                if major >= 2 and minor >= 0 and patch >= 13:
                    return parent.FindFirst(uiautomation.ControlType.Any, {"AutomationId": automation_id})
                else:
                    # 兼容旧版本API
                    return parent.FindFirst(None, {"AutomationId": automation_id})
            else:
                # 未知版本，使用兼容方式
                return parent.FindFirst(None, {"AutomationId": automation_id})
        except Exception as e:
            print(f"根据Automation ID查找元素失败: {e}")
            return None
    
    @staticmethod
    def get_element_by_name(parent, name):
        """根据名称获取元素，兼容不同版本的uiautomation库
        
        Args:
            parent: 父元素
            name: 元素名称
            
        Returns:
            找到的元素，找不到返回None
        """
        try:
            if hasattr(uiautomation, '__version__'):
                version_parts = uiautomation.__version__.split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1])
                
                if major >= 2 and minor >= 0:
                    return parent.FindFirst(uiautomation.ControlType.Any, {"Name": name})
                else:
                    return parent.FindFirst(None, {"Name": name})
            else:
                return parent.FindFirst(None, {"Name": name})
        except Exception as e:
            print(f"根据名称查找元素失败: {e}")
            return None
    
    @staticmethod
    def get_element_by_class(parent, class_name):
        """根据类名获取元素，兼容不同版本的uiautomation库
        
        Args:
            parent: 父元素
            class_name: 类名
            
        Returns:
            找到的元素，找不到返回None
        """
        try:
            if hasattr(uiautomation, '__version__'):
                version_parts = uiautomation.__version__.split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1])
                
                if major >= 2 and minor >= 0:
                    return parent.FindFirst(uiautomation.ControlType.Any, {"ClassName": class_name})
                else:
                    return parent.FindFirst(None, {"ClassName": class_name})
            else:
                return parent.FindFirst(None, {"ClassName": class_name})
        except Exception as e:
            print(f"根据类名查找元素失败: {e}")
            return None
    
    @staticmethod
    def get_children(parent):
        """获取子元素列表，兼容不同版本的uiautomation库
        
        Args:
            parent: 父元素
            
        Returns:
            子元素列表
        """
        try:
            if hasattr(uiautomation, '__version__'):
                version_parts = uiautomation.__version__.split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1])
                
                if major >= 2 and minor >= 0:
                    return parent.GetChildren()
                else:
                    return parent.GetChildren()
            else:
                return parent.GetChildren()
        except Exception as e:
            print(f"获取子元素失败: {e}")
            return []
    
    @staticmethod
    def get_bounding_rectangle(element):
        """获取元素的边界矩形，兼容不同版本的uiautomation库
        
        Args:
            element: 元素对象
            
        Returns:
            边界矩形对象，包含left, top, right, bottom属性
        """
        try:
            if hasattr(element, 'BoundingRectangle'):
                return element.BoundingRectangle
            elif hasattr(element, 'Rectangle'):
                return element.Rectangle
            else:
                raise AttributeError("元素没有边界矩形属性")
        except Exception as e:
            print(f"获取元素边界矩形失败: {e}")
            return None
    
    @staticmethod
    def get_element_info(pywinauto_element):
        """获取pywinauto元素的信息，兼容不同版本的pywinauto库
        
        Args:
            pywinauto_element: pywinauto元素对象
            
        Returns:
            元素信息对象
        """
        try:
            if hasattr(pywinauto_element, 'element_info'):
                return pywinauto_element.element_info
            elif hasattr(pywinauto_element, 'info'):
                return pywinauto_element.info
            else:
                raise AttributeError("元素没有信息属性")
        except Exception as e:
            print(f"获取pywinauto元素信息失败: {e}")
            return None
    
    @staticmethod
    def get_control_type(element_info):
        """获取元素的控制类型，兼容不同版本的pywinauto库
        
        Args:
            element_info: 元素信息对象
            
        Returns:
            控制类型字符串
        """
        try:
            if hasattr(element_info, 'control_type'):
                return element_info.control_type
            elif hasattr(element_info, 'control_type_name'):
                return element_info.control_type_name
            else:
                return "Unknown"
        except Exception as e:
            print(f"获取元素控制类型失败: {e}")
            return "Unknown"
    
    @staticmethod
    def get_automation_id(element_info):
        """获取元素的Automation ID，兼容不同版本的pywinauto库
        
        Args:
            element_info: 元素信息对象
            
        Returns:
            Automation ID字符串
        """
        try:
            if hasattr(element_info, 'automation_id'):
                return element_info.automation_id
            elif hasattr(element_info, 'automationId'):
                return element_info.automationId
            else:
                return ""
        except Exception as e:
            print(f"获取元素Automation ID失败: {e}")
            return ""
    
    @staticmethod
    def get_class_name(element_info):
        """获取元素的类名，兼容不同版本的pywinauto库
        
        Args:
            element_info: 元素信息对象
            
        Returns:
            类名字符串
        """
        try:
            if hasattr(element_info, 'class_name'):
                return element_info.class_name
            elif hasattr(element_info, 'ClassName'):
                return element_info.ClassName
            else:
                return ""
        except Exception as e:
            print(f"获取元素类名失败: {e}")
            return ""
    
    @staticmethod
    def get_name(element_info):
        """获取元素的名称，兼容不同版本的pywinauto库
        
        Args:
            element_info: 元素信息对象
            
        Returns:
            名称字符串
        """
        try:
            if hasattr(element_info, 'name'):
                return element_info.name
            elif hasattr(element_info, 'Name'):
                return element_info.Name
            else:
                return ""
        except Exception as e:
            print(f"获取元素名称失败: {e}")
            return ""
    
    @staticmethod
    def get_rectangle(element_info):
        """获取元素的矩形信息，兼容不同版本的pywinauto库
        
        Args:
            element_info: 元素信息对象
            
        Returns:
            矩形对象，包含left, top, width, height属性
        """
        try:
            if hasattr(element_info, 'rectangle'):
                return element_info.rectangle
            elif hasattr(element_info, 'Rectangle'):
                return element_info.Rectangle
            else:
                raise AttributeError("元素没有矩形属性")
        except Exception as e:
            print(f"获取元素矩形信息失败: {e}")
            return None
