#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件管理器模块
负责插件的加载、管理和调用
"""

import os
import sys
import importlib.util
import inspect
from .plugin_interface import BasePlugin, LocatorPlugin, CodeGeneratorPlugin, ExportPlugin


class PluginManager:
    """插件管理器类"""
    
    def __init__(self):
        """初始化插件管理器"""
        self.plugins = []
        self.locator_plugins = []
        self.code_generator_plugins = []
        self.export_plugins = []
        self.plugin_dirs = [
            os.path.join(os.path.dirname(__file__), '..', 'plugins'),
            os.path.join(os.path.expanduser('~'), '.locator_desktop', 'plugins')
        ]
    
    def add_plugin_dir(self, plugin_dir):
        """添加插件目录
        
        Args:
            plugin_dir: 插件目录路径
        """
        if plugin_dir not in self.plugin_dirs:
            self.plugin_dirs.append(plugin_dir)
    
    def load_plugins(self):
        """加载所有插件"""
        # 清空现有插件列表
        self.plugins = []
        self.locator_plugins = []
        self.code_generator_plugins = []
        self.export_plugins = []
        
        # 扫描所有插件目录
        for plugin_dir in self.plugin_dirs:
            if os.path.exists(plugin_dir):
                self._load_plugins_from_dir(plugin_dir)
    
    def _load_plugins_from_dir(self, plugin_dir):
        """从指定目录加载插件
        
        Args:
            plugin_dir: 插件目录路径
        """
        # 添加插件目录到Python路径
        if plugin_dir not in sys.path:
            sys.path.append(plugin_dir)
        
        # 遍历目录下的所有.py文件
        for file_name in os.listdir(plugin_dir):
            file_path = os.path.join(plugin_dir, file_name)
            if file_name.endswith('.py') and os.path.isfile(file_path):
                self._load_plugin_from_file(file_path)
            elif os.path.isdir(file_path) and os.path.exists(os.path.join(file_path, '__init__.py')):
                # 处理包形式的插件
                self._load_plugin_from_package(file_path)
    
    def _load_plugin_from_file(self, file_path):
        """从文件加载插件
        
        Args:
            file_path: 插件文件路径
        """
        try:
            # 获取模块名称
            module_name = os.path.basename(file_path)[:-3]
            
            # 加载模块
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 查找插件类
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BasePlugin) and cls != BasePlugin:
                    # 实例化插件
                    plugin_instance = cls()
                    self._register_plugin(plugin_instance)
        except Exception as e:
            print(f"加载插件 {file_path} 失败: {e}")
    
    def _load_plugin_from_package(self, package_path):
        """从包加载插件
        
        Args:
            package_path: 插件包路径
        """
        try:
            # 获取包名称
            package_name = os.path.basename(package_path)
            
            # 加载包
            spec = importlib.util.spec_from_file_location(package_name, os.path.join(package_path, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[package_name] = module
            spec.loader.exec_module(module)
            
            # 查找插件类
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BasePlugin) and cls != BasePlugin:
                    # 实例化插件
                    plugin_instance = cls()
                    self._register_plugin(plugin_instance)
        except Exception as e:
            print(f"加载插件包 {package_path} 失败: {e}")
    
    def _register_plugin(self, plugin):
        """注册插件
        
        Args:
            plugin: 插件实例
        """
        # 添加到所有插件列表
        self.plugins.append(plugin)
        
        # 根据插件类型添加到对应列表
        if isinstance(plugin, LocatorPlugin):
            self.locator_plugins.append(plugin)
        elif isinstance(plugin, CodeGeneratorPlugin):
            self.code_generator_plugins.append(plugin)
        elif isinstance(plugin, ExportPlugin):
            self.export_plugins.append(plugin)
    
    def initialize_plugins(self, app):
        """初始化所有插件
        
        Args:
            app: 主应用实例
        """
        for plugin in self.plugins:
            try:
                plugin.initialize(app)
            except Exception as e:
                print(f"初始化插件 {plugin.name} 失败: {e}")
    
    def shutdown_plugins(self):
        """关闭所有插件"""
        for plugin in self.plugins:
            try:
                plugin.shutdown()
            except Exception as e:
                print(f"关闭插件 {plugin.name} 失败: {e}")
    
    def get_all_plugins(self):
        """获取所有插件
        
        Returns:
            插件列表
        """
        return self.plugins
    
    def get_locator_plugins(self):
        """获取所有定位插件
        
        Returns:
            定位插件列表
        """
        return self.locator_plugins
    
    def get_code_generator_plugins(self):
        """获取所有代码生成插件
        
        Returns:
            代码生成插件列表
        """
        return self.code_generator_plugins
    
    def get_export_plugins(self):
        """获取所有导出插件
        
        Returns:
            导出插件列表
        """
        return self.export_plugins
    
    def get_plugin_by_name(self, name):
        """根据名称获取插件
        
        Args:
            name: 插件名称
            
        Returns:
            插件实例，未找到返回None
        """
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None
    
    def get_locator_plugin_by_name(self, name):
        """根据名称获取定位插件
        
        Args:
            name: 插件名称
            
        Returns:
            定位插件实例，未找到返回None
        """
        for plugin in self.locator_plugins:
            if plugin.name == name:
                return plugin
        return None
    
    def get_code_generator_plugin_by_language(self, language):
        """根据语言名称获取代码生成插件
        
        Args:
            language: 语言名称
            
        Returns:
            代码生成插件实例，未找到返回None
        """
        for plugin in self.code_generator_plugins:
            if plugin.get_language_name() == language:
                return plugin
        return None
    
    def get_export_plugin_by_format(self, format_name):
        """根据格式名称获取导出插件
        
        Args:
            format_name: 格式名称
            
        Returns:
            导出插件实例，未找到返回None
        """
        for plugin in self.export_plugins:
            if plugin.get_export_format() == format_name:
                return plugin
        return None
    
    def generate_plugin_info(self):
        """生成插件信息
        
        Returns:
            包含所有插件信息的字典
        """
        plugin_info = {
            "total_plugins": len(self.plugins),
            "locator_plugins": [plugin.get_info() for plugin in self.locator_plugins],
            "code_generator_plugins": [plugin.get_info() for plugin in self.code_generator_plugins],
            "export_plugins": [plugin.get_info() for plugin in self.export_plugins],
            "all_plugins": [plugin.get_info() for plugin in self.plugins]
        }
        return plugin_info
