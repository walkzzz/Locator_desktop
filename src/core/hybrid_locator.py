# -*- coding: utf-8 -*-
"""
混合定位器模块，实现混合定位策略
"""

from typing import List, Dict, Any
from .element import Element
from .locator_strategy import LocatorMethod


class HybridLocator:
    """混合定位器类，实现多种定位方法的结合使用"""
    
    def __init__(self, element_capture, code_generator):
        """初始化混合定位器
        
        Args:
            element_capture: 元素捕获实例
            code_generator: 代码生成器实例
        """
        self.element_capture = element_capture
        self.code_generator = code_generator
    
    def locate_element(self, element_info: Dict[str, Any], window_handle: int = None) -> Element:
        """使用混合定位策略定位元素
        
        Args:
            element_info: 元素信息字典，包含各种定位属性
            window_handle: 窗口句柄，可选
            
        Returns:
            定位到的元素对象，或None
        """
        # 定义定位方法优先级顺序
        locator_order = [
            self._attribute_locator,
            self._image_locator,
            self._coordinate_locator
        ]
        
        # 尝试各种定位方法，直到成功
        for locator_func in locator_order:
            try:
                element = locator_func(element_info, window_handle)
                if element:
                    return element
            except Exception as e:
                print(f"{locator_func.__name__}定位失败: {e}")
                continue
        
        return None
    
    def _attribute_locator(self, element_info: Dict[str, Any], window_handle: int = None) -> Element:
        """使用属性定位元素
        
        Args:
            element_info: 元素信息字典
            window_handle: 窗口句柄
            
        Returns:
            定位到的元素对象，或None
        """
        # 检查是否有足够的属性用于定位
        if not any(key in element_info for key in ['automation_id', 'name', 'class_name']):
            return None
        
        # 创建元素对象
        element = Element()
        
        # 填充元素属性
        for key, value in element_info.items():
            if hasattr(element, key):
                setattr(element, key, value)
        
        # 测试定位
        if window_handle:
            element.window_handle = window_handle
            if self.element_capture.test_element_location(element):
                return element
        
        return None
    
    def _image_locator(self, element_info: Dict[str, Any], window_handle: int = None) -> Element:
        """使用图像识别定位元素
        
        Args:
            element_info: 元素信息字典，需要包含image_path
            window_handle: 窗口句柄
            
        Returns:
            定位到的元素对象，或None
        """
        if 'image_path' not in element_info:
            return None
        
        # 使用图像识别捕获元素
        return self.element_capture.capture_element_by_image(
            element_info['image_path'],
            element_info.get('confidence', 0.8)
        )
    
    def _coordinate_locator(self, element_info: Dict[str, Any], window_handle: int = None) -> Element:
        """使用坐标定位元素
        
        Args:
            element_info: 元素信息字典，需要包含x和y坐标
            window_handle: 窗口句柄
            
        Returns:
            定位到的元素对象，或None
        """
        if not all(key in element_info for key in ['x', 'y']):
            return None
        
        # 从坐标创建元素对象
        element = Element()
        element.x = element_info['x']
        element.y = element_info['y']
        element.width = element_info.get('width', 0)
        element.height = element_info.get('height', 0)
        element.window_handle = window_handle
        
        return element
    
    def generate_hybrid_code(self, element: Element) -> Dict[LocatorMethod, str]:
        """生成混合定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            不同定位方法的代码字典
        """
        # 生成各种定位方法的代码
        code_dict = {
            LocatorMethod.ATTRIBUTE: self.code_generator.generate_pywinauto_code(element),
            LocatorMethod.IMAGE: self.code_generator.generate_image_recognition_code(element),
            LocatorMethod.COORDINATE: self.code_generator.generate_coordinate_code(element)
        }
        
        # 生成uiautomation代码
        if hasattr(self.code_generator, 'generate_uiautomation_code'):
            code_dict[LocatorMethod.ATTRIBUTE] = self.code_generator.generate_uiautomation_code(element)
        
        return code_dict
    
    def get_optimized_locator_code(self, element: Element) -> str:
        """获取优化的定位代码
        
        Args:
            element: 元素对象，包含locator_strategy属性
            
        Returns:
            优化的定位代码字符串
        """
        if not element or not hasattr(element, 'locator_strategy'):
            # 默认使用属性定位
            return self.code_generator.generate_pywinauto_code(element)
        
        # 根据推荐的定位策略生成代码
        if element.locator_strategy == LocatorMethod.ATTRIBUTE:
            return self.code_generator.generate_pywinauto_code(element)
        elif element.locator_strategy == LocatorMethod.IMAGE:
            return self.code_generator.generate_image_recognition_code(element)
        elif element.locator_strategy == LocatorMethod.COORDINATE:
            return self.code_generator.generate_coordinate_code(element)
        elif element.locator_strategy == LocatorMethod.HYBRID:
            # 生成包含多种定位方法的混合代码
            return self._generate_hybrid_fallback_code(element)
        else:
            # 默认使用属性定位
            return self.code_generator.generate_pywinauto_code(element)
    
    def _generate_hybrid_fallback_code(self, element: Element) -> str:
        """生成带有回退机制的混合定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            带有回退机制的定位代码字符串
        """
        # 生成带有try-except结构的代码，包含多种定位方法
        pywinauto_code = self.code_generator.generate_pywinauto_code(element)
        image_code = self.code_generator.generate_image_recognition_code(element)
        coordinate_code = self.code_generator.generate_coordinate_code(element)
        
        # 构建带有回退机制的代码
        fallback_code = f"""try:
    # 优先使用pywinauto属性定位
    {pywinauto_code}
except Exception as e:
    print(f\"pywinauto定位失败: {{{e}}}")
    try:
        # 回退到图像识别定位
        {image_code}
    except Exception as e:
        print(f\"图像识别定位失败: {{{e}}}")
        # 最后回退到坐标定位
        {coordinate_code}
"""
        
        return fallback_code
