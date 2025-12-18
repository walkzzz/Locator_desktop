#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件接口定义模块
定义插件必须实现的接口
"""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """插件基类，所有插件必须继承此类并实现抽象方法"""
    
    def __init__(self):
        """初始化插件"""
        self.name = "BasePlugin"
        self.version = "1.0.0"
        self.author = "Unknown"
        self.description = "基础插件类"
    
    @abstractmethod
    def initialize(self, app):
        """初始化插件
        
        Args:
            app: 主应用实例
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """关闭插件"""
        pass
    
    def get_info(self):
        """获取插件信息
        
        Returns:
            包含插件信息的字典
        """
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description
        }


class LocatorPlugin(BasePlugin):
    """定位插件接口，用于扩展定位方法"""
    
    @abstractmethod
    def get_locator_name(self):
        """获取定位方法名称
        
        Returns:
            定位方法名称字符串
        """
        pass
    
    @abstractmethod
    def locate_element(self, element, **kwargs):
        """定位元素
        
        Args:
            element: 元素对象
            **kwargs: 其他参数
            
        Returns:
            定位结果，成功返回True，失败返回False
        """
        pass
    
    @abstractmethod
    def generate_locator_code(self, element, **kwargs):
        """生成定位代码
        
        Args:
            element: 元素对象
            **kwargs: 其他参数
            
        Returns:
            生成的定位代码字符串
        """
        pass


class CodeGeneratorPlugin(BasePlugin):
    """代码生成插件接口，用于扩展代码生成格式"""
    
    @abstractmethod
    def get_language_name(self):
        """获取生成代码的语言名称
        
        Returns:
            语言名称字符串
        """
        pass
    
    @abstractmethod
    def generate_code(self, element, **kwargs):
        """生成代码
        
        Args:
            element: 元素对象
            **kwargs: 其他参数
            
        Returns:
            生成的代码字符串
        """
        pass


class ExportPlugin(BasePlugin):
    """导出插件接口，用于扩展导出格式"""
    
    @abstractmethod
    def get_export_format(self):
        """获取导出格式名称
        
        Returns:
            导出格式名称字符串
        """
        pass
    
    @abstractmethod
    def export(self, data, file_path, **kwargs):
        """执行导出
        
        Args:
            data: 要导出的数据
            file_path: 导出文件路径
            **kwargs: 其他参数
            
        Returns:
            导出是否成功
        """
        pass
