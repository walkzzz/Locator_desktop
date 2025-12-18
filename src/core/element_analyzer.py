#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinauto

from .element import Element


class ElementAnalyzer:
    """元素分析器类，负责分析窗口的UI元素结构"""

    def __init__(self):
        self.max_depth = 10  # 最大分析深度
        self.initial_load_depth = 3  # 初始加载深度，可见层级
        
        # 元素树缓存，键为 (process_id, window_handle)，值为 (element_tree, timestamp)
        self.element_tree_cache = {}
        self.cache_expiry_time = 600  # 缓存过期时间，单位：秒（10分钟）
    
    def analyze_window(self, window):
        """分析窗口的UI元素结构，支持缓存机制
        
        Args:
            window: 窗口对象，包含hwnd属性
            
        Returns:
            根元素对象，分析失败返回None
        """
        if not hasattr(window, 'hwnd'):
            print("无效的窗口对象")
            return None
        
        import time
        
        try:
            window_handle = window.hwnd
            
            # 获取进程ID
            import win32process
            _, process_id = win32process.GetWindowThreadProcessId(window_handle)
            
            # 检查缓存
            cache_key = (process_id, window_handle)
            current_time = time.time()
            
            if cache_key in self.element_tree_cache:
                # 检查缓存是否过期
                cached_element_tree, cached_time = self.element_tree_cache[cache_key]
                if current_time - cached_time < self.cache_expiry_time:
                    print(f"使用缓存的元素树，缓存时间: {time.ctime(cached_time)}")
                    return cached_element_tree
                else:
                    # 缓存过期，删除缓存
                    print(f"缓存过期，重新分析窗口，过期时间: {time.ctime(cached_time)}")
                    del self.element_tree_cache[cache_key]
            
            # 使用pywinauto分析窗口
            app = pywinauto.Application(backend='uia').connect(handle=window_handle)
            window_element = app.window(handle=window_handle)
            
            # 转换为自定义Element对象
            root_element = self._convert_pywinauto_to_element(window_element.element_info)
            
            # 递归分析子元素
            self._analyze_element_children(window_element, root_element, 1)
            
            # 缓存元素树
            self.element_tree_cache[cache_key] = (root_element, current_time)
            print(f"元素树已缓存，缓存键: {cache_key}")
            
            return root_element
        except Exception as e:
            print(f"分析窗口元素失败: {e}")
            return None
    
    def _analyze_element_children(self, parent_pywinauto_element, parent_element, current_depth):
        """递归分析元素的子元素，支持分层懒加载
        
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
                
                # 检查是否需要加载子元素
                if current_depth < self.initial_load_depth:
                    # 当前深度小于初始加载深度，递归加载子元素
                    self._analyze_element_children(child_pywinauto_element, child_element, current_depth + 1)
                else:
                    # 当前深度达到初始加载深度，标记该元素有子元素但未加载
                    child_element.has_children = True
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
    
    def calculate_stability_score(self, element):
        """计算元素定位稳定性评分
        
        Args:
            element: 元素对象
            
        Returns:
            稳定性评分（0-100）
        """
        if not element:
            return 0
        
        # 初始化评分
        score = 0
        suggestions = []
        locator_scores = {}
        
        # 基于属性完整性的评分
        if element.automation_id:
            score += 35
            locator_scores['automation_id'] = 35
        else:
            suggestions.append("缺少Automation ID，建议优先使用具有稳定Automation ID的元素")
        
        if element.name:
            # 检查名称是否为动态值
            if len(element.name) > 5 and not any(char.isdigit() for char in element.name):
                score += 25
                locator_scores['name'] = 25
            else:
                score += 15
                locator_scores['name'] = 15
                suggestions.append("元素名称较短或包含数字，可能是动态生成的")
        else:
            suggestions.append("缺少元素名称，定位稳定性可能较差")
        
        if element.class_name:
            score += 20
            locator_scores['class_name'] = 20
        else:
            suggestions.append("缺少类名，定位稳定性可能较差")
        
        if element.control_type:
            score += 15
            locator_scores['control_type'] = 15
        else:
            suggestions.append("缺少控件类型，定位稳定性可能较差")
        
        if element.depth > 5:
            score -= 10
            suggestions.append(f"元素层级较深（深度: {element.depth}），建议优化定位路径")
        
        # 确保评分在0-100范围内
        score = max(0, min(100, score))
        
        # 更新元素属性
        element.stability_score = score
        element.stability_suggestions = suggestions
        element.locator_scores = locator_scores
        
        # 推荐最佳定位策略
        self.recommend_locator_strategy(element)
        
        return score
    
    def recommend_locator_strategy(self, element):
        """推荐最佳定位策略
        
        Args:
            element: 元素对象
        """
        if not element:
            return
        
        # 基于稳定性评分推荐定位策略
        if element.stability_score >= 80:
            # 高稳定性，优先使用属性定位
            best_locator = "attribute"
        elif element.stability_score >= 50:
            # 中等稳定性，建议使用属性+图像混合定位
            best_locator = "hybrid"
        else:
            # 低稳定性，建议使用图像定位
            best_locator = "image"
        
        # 基于属性优先级排序定位方法
        locator_priority = []
        
        if element.automation_id:
            locator_priority.append("automation_id")
        
        if element.name and len(element.name) > 5 and not any(char.isdigit() for char in element.name):
            locator_priority.append("name")
        
        if element.class_name:
            locator_priority.append("class_name")
        
        if element.control_type:
            locator_priority.append("control_type")
        
        # 添加坐标和图像定位作为备选
        locator_priority.append("coordinate")
        locator_priority.append("image")
        
        # 更新元素属性
        element.locator_strategy = best_locator
        element.locator_priority = locator_priority
