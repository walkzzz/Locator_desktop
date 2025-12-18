#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Element:
    """UI元素类，用于表示和存储UI元素的各种属性"""

    def __init__(self):
        # 元素基本信息
        self.element_id = None  # 元素唯一标识
        self.name = None        # 元素名称
        self.element_type = None  # 元素类型
        self.control_type = None  # 控件类型
        self.class_name = None   # 类名
        self.automation_id = None  # Automation ID
        
        # 元素位置和尺寸
        self.x = None           # 元素左上角x坐标
        self.y = None           # 元素左上角y坐标
        self.width = None       # 元素宽度
        self.height = None      # 元素高度
        
        # 元素层次结构
        self.parent = None      # 父元素
        self.children = []      # 子元素列表
        self.depth = 0          # 元素深度
        
        # 元素状态和属性
        self.is_enabled = None  # 是否可用
        self.is_visible = None  # 是否可见
        self.is_checked = None  # 是否被选中（针对复选框、单选按钮等）
        self.text = None        # 元素文本内容
        
        # 其他属性
        self.process_id = None  # 所属进程ID
        self.window_handle = None  # 所属窗口句柄
        
        # 元素特定属性
        self.attributes = {}    # 其他自定义属性
    
    def __str__(self):
        """字符串表示"""
        return f"{self.element_type} - {self.name or 'Unnamed'} ({self.x}, {self.y}) [{self.width}x{self.height}]"
    
    def add_child(self, child):
        """添加子元素
        
        Args:
            child: 子元素对象
        """
        child.parent = self
        child.depth = self.depth + 1
        self.children.append(child)
    
    def get_path(self):
        """获取元素路径
        
        Returns:
            元素路径字符串
        """
        path = []
        current = self
        while current:
            path.append(f"{current.element_type}({current.name or 'Unnamed'})")
            current = current.parent
        return ' > '.join(reversed(path))
