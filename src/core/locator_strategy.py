# -*- coding: utf-8 -*-
"""
定位策略评估和选择模块
"""

from enum import Enum
from typing import List, Dict, Any


class LocatorMethod(Enum):
    """定位方法枚举"""
    ATTRIBUTE = "attribute"
    IMAGE = "image"
    COORDINATE = "coordinate"
    HYBRID = "hybrid"


class LocatorStrategy:
    """定位策略评估和选择类"""
    
    def __init__(self):
        self.strategy_scores = {
            LocatorMethod.ATTRIBUTE: 0,
            LocatorMethod.IMAGE: 0,
            LocatorMethod.COORDINATE: 0
        }
    
    def evaluate_element(self, element: Any) -> Dict[LocatorMethod, int]:
        """评估元素适合的定位方法
        
        Args:
            element: 元素对象
            
        Returns:
            各定位方法的评分字典
        """
        # 重置评分
        for method in self.strategy_scores:
            self.strategy_scores[method] = 0
        
        # 评估属性定位
        self._evaluate_attribute_strategy(element)
        
        # 评估图像识别定位
        self._evaluate_image_strategy(element)
        
        # 评估坐标定位
        self._evaluate_coordinate_strategy(element)
        
        return self.strategy_scores.copy()
    
    def _evaluate_attribute_strategy(self, element: Any):
        """评估属性定位策略
        
        Args:
            element: 元素对象
        """
        score = 0
        
        # automation_id 是最稳定的属性
        if hasattr(element, 'automation_id') and element.automation_id:
            score += 50
        
        # class_name 相对稳定
        if hasattr(element, 'class_name') and element.class_name:
            score += 30
        
        # name 可能是动态的
        if hasattr(element, 'name') and element.name:
            score += 20
        
        # 检查是否有足够的属性
        if score >= 50:
            self.strategy_scores[LocatorMethod.ATTRIBUTE] = score
        else:
            # 如果属性不足，降低评分
            self.strategy_scores[LocatorMethod.ATTRIBUTE] = max(score - 30, 0)
    
    def _evaluate_image_strategy(self, element: Any):
        """评估图像识别定位策略
        
        Args:
            element: 元素对象
        """
        score = 0
        
        # 检查元素尺寸
        if (hasattr(element, 'width') and element.width > 10 and
            hasattr(element, 'height') and element.height > 10):
            score += 40
        
        # 检查元素类型
        if hasattr(element, 'element_type') and element.element_type in ['Button', 'Image', 'MenuItem']:
            score += 30
        
        # 检查是否有属性定位的可能
        if self.strategy_scores[LocatorMethod.ATTRIBUTE] < 50:
            # 如果属性定位不可靠，提升图像识别评分
            score += 30
        
        self.strategy_scores[LocatorMethod.IMAGE] = min(score, 100)
    
    def _evaluate_coordinate_strategy(self, element: Any):
        """评估坐标定位策略
        
        Args:
            element: 元素对象
        """
        score = 20  # 坐标定位基础分较低
        
        # 检查是否有其他定位方式
        if self.strategy_scores[LocatorMethod.ATTRIBUTE] < 30 and self.strategy_scores[LocatorMethod.IMAGE] < 30:
            # 如果其他定位方式都不可靠，提升坐标定位评分
            score += 30
        
        self.strategy_scores[LocatorMethod.COORDINATE] = min(score, 100)
    
    def select_best_strategy(self, scores: Dict[LocatorMethod, int]) -> LocatorMethod:
        """选择最佳定位策略
        
        Args:
            scores: 各定位方法的评分字典
            
        Returns:
            最佳定位方法
        """
        # 找到评分最高的定位方法
        best_method = max(scores, key=scores.get)
        best_score = scores[best_method]
        
        # 如果属性定位评分很高，直接使用属性定位
        if best_method == LocatorMethod.ATTRIBUTE and best_score >= 70:
            return LocatorMethod.ATTRIBUTE
        
        # 如果图像识别评分很高，直接使用图像识别
        if best_method == LocatorMethod.IMAGE and best_score >= 70:
            return LocatorMethod.IMAGE
        
        # 如果坐标定位是唯一选择，使用坐标定位
        if best_score > 0 and all(score <= best_score for score in scores.values()):
            return LocatorMethod.HYBRID
        
        # 默认使用混合定位
        return LocatorMethod.HYBRID
    
    def get_hybrid_strategy(self, scores: Dict[LocatorMethod, int]) -> List[LocatorMethod]:
        """获取混合定位策略序列
        
        Args:
            scores: 各定位方法的评分字典
            
        Returns:
            混合定位策略序列，按优先级排序
        """
        # 按评分排序，筛选分数大于0的方法
        sorted_methods = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        active_methods = [method for method, score in sorted_methods if score > 0]
        
        # 如果没有有效方法，返回默认策略
        if not active_methods:
            return [LocatorMethod.ATTRIBUTE, LocatorMethod.IMAGE, LocatorMethod.COORDINATE]
        
        # 如果只有一个有效方法，直接返回
        if len(active_methods) == 1:
            return active_methods
        
        # 构建混合策略
        hybrid_strategy = []
        
        # 优先添加属性定位
        if LocatorMethod.ATTRIBUTE in active_methods:
            hybrid_strategy.append(LocatorMethod.ATTRIBUTE)
        
        # 然后添加图像识别
        if LocatorMethod.IMAGE in active_methods:
            hybrid_strategy.append(LocatorMethod.IMAGE)
        
        # 最后添加坐标定位
        if LocatorMethod.COORDINATE in active_methods:
            hybrid_strategy.append(LocatorMethod.COORDINATE)
        
        return hybrid_strategy
    
    def get_strategy_name(self, method: LocatorMethod) -> str:
        """获取定位策略名称
        
        Args:
            method: 定位方法
            
        Returns:
            定位策略名称
        """
        name_map = {
            LocatorMethod.ATTRIBUTE: "属性定位",
            LocatorMethod.IMAGE: "图像识别定位",
            LocatorMethod.COORDINATE: "坐标定位",
            LocatorMethod.HYBRID: "混合定位"
        }
        return name_map.get(method, "未知定位")


# 全局定位策略实例
locator_strategy = LocatorStrategy()