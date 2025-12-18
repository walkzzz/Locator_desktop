# -*- coding: utf-8 -*-
"""
定位稳定性评分模块
"""

from typing import Dict, Any


class StabilityAnalyzer:
    """定位稳定性分析器类"""
    
    def __init__(self):
        # 各属性的权重配置
        self.attribute_weights = {
            'automation_id': 0.4,  # 最稳定的属性
            'class_name': 0.3,      # 稳定的属性
            'name': 0.2,            # 可能动态的属性
            'control_type': 0.1      # 控件类型
        }
        
        # 层级深度权重
        self.depth_weight = 0.2
        
        # 元素可见性权重
        self.visibility_weight = 0.1
        
        # 元素可用性权重
        self.enabled_weight = 0.1
    
    def calculate_stability_score(self, element: Any, element_path: str = None) -> Dict[str, Any]:
        """计算定位稳定性评分
        
        Args:
            element: 元素对象
            element_path: 元素路径，用于分析层级深度
            
        Returns:
            包含稳定性评分和优化建议的字典
        """
        # 初始化结果
        result = {
            'score': 0,
            'attribute_scores': {},
            'depth_score': 0,
            'visibility_score': 0,
            'enabled_score': 0,
            'suggestions': []
        }
        
        # 计算属性稳定性评分
        result['attribute_scores'] = self._calculate_attribute_score(element)
        attribute_total = sum(score for score in result['attribute_scores'].values())
        attribute_weighted = attribute_total * sum(self.attribute_weights.values())
        
        # 计算层级深度评分
        result['depth_score'] = self._calculate_depth_score(element_path)
        depth_weighted = result['depth_score'] * self.depth_weight
        
        # 计算可见性评分
        result['visibility_score'] = self._calculate_visibility_score(element)
        visibility_weighted = result['visibility_score'] * self.visibility_weight
        
        # 计算可用性评分
        result['enabled_score'] = self._calculate_enabled_score(element)
        enabled_weighted = result['enabled_score'] * self.enabled_weight
        
        # 计算总评分
        result['score'] = int(attribute_weighted + depth_weighted + visibility_weighted + enabled_weighted)
        
        # 生成优化建议
        result['suggestions'] = self._generate_suggestions(element, result)
        
        return result
    
    def _calculate_attribute_score(self, element: Any) -> Dict[str, int]:
        """计算属性稳定性评分
        
        Args:
            element: 元素对象
            
        Returns:
            各属性的稳定性评分字典
        """
        attribute_scores = {}
        
        # automation_id 评分
        if hasattr(element, 'automation_id') and element.automation_id:
            # automation_id 是最稳定的属性
            attribute_scores['automation_id'] = 100
        else:
            attribute_scores['automation_id'] = 0
            
        # class_name 评分
        if hasattr(element, 'class_name') and element.class_name:
            # class_name 相对稳定
            attribute_scores['class_name'] = 80
        else:
            attribute_scores['class_name'] = 0
            
        # name 评分
        if hasattr(element, 'name') and element.name:
            # 检查 name 是否可能是动态生成的
            if self._is_dynamic_name(element.name):
                # 动态 name 评分较低
                attribute_scores['name'] = 40
            else:
                # 静态 name 评分较高
                attribute_scores['name'] = 70
        else:
            attribute_scores['name'] = 0
            
        # control_type 评分
        if hasattr(element, 'control_type') and element.control_type:
            attribute_scores['control_type'] = 90
        else:
            attribute_scores['control_type'] = 0
            
        return attribute_scores
    
    def _is_dynamic_name(self, name: str) -> bool:
        """检查名称是否是动态生成的
        
        Args:
            name: 元素名称
            
        Returns:
            是否是动态名称
        """
        import re
        
        # 检查是否包含数字序列
        if re.search(r'\d{4,}', name):
            return True
            
        # 检查是否包含特殊字符组合
        if re.search(r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}', name):
            return True  # UUID 格式
            
        # 检查是否包含时间戳格式
        if re.search(r'\d{14}', name):
            return True  # 年月日时分秒格式
            
        # 检查名称长度是否过长
        if len(name) > 100:
            return True
            
        return False
    
    def _calculate_depth_score(self, element_path: str) -> int:
        """计算层级深度评分
        
        Args:
            element_path: 元素路径
            
        Returns:
            层级深度评分
        """
        if not element_path:
            return 50
            
        # 计算路径中的层级数量
        depth = element_path.count('>') + 1
        
        # 深度越小，评分越高
        if depth <= 3:
            return 100
        elif depth <= 5:
            return 80
        elif depth <= 7:
            return 60
        elif depth <= 10:
            return 40
        else:
            return 20
    
    def _calculate_visibility_score(self, element: Any) -> int:
        """计算可见性评分
        
        Args:
            element: 元素对象
            
        Returns:
            可见性评分
        """
        if hasattr(element, 'is_visible'):
            if element.is_visible:
                return 100
            else:
                return 30
        return 50
    
    def _calculate_enabled_score(self, element: Any) -> int:
        """计算可用性评分
        
        Args:
            element: 元素对象
            
        Returns:
            可用性评分
        """
        if hasattr(element, 'is_enabled'):
            if element.is_enabled:
                return 100
            else:
                return 50
        return 70
    
    def _generate_suggestions(self, element: Any, stability_result: Dict[str, Any]) -> list:
        """生成优化建议
        
        Args:
            element: 元素对象
            stability_result: 稳定性分析结果
            
        Returns:
            优化建议列表
        """
        suggestions = []
        
        # 检查是否缺少 automation_id
        if stability_result['attribute_scores']['automation_id'] == 0:
            if hasattr(element, 'name') and element.name:
                suggestions.append(f"当前使用名称 '{element.name}' 进行定位，建议替换为更稳定的 automation_id（如果可用）")
            elif hasattr(element, 'class_name') and element.class_name:
                suggestions.append(f"当前使用类名 '{element.class_name}' 进行定位，建议替换为更稳定的 automation_id（如果可用）")
        
        # 检查名称是否动态
        if hasattr(element, 'name') and element.name:
            if self._is_dynamic_name(element.name):
                suggestions.append(f"元素名称 '{element.name}' 可能是动态生成的，建议使用更稳定的属性")
        
        # 检查层级是否过深
        if stability_result['depth_score'] < 50:
            suggestions.append(f"元素层级较深，定位可能不稳定，建议简化定位路径")
        
        # 检查元素是否可见
        if stability_result['visibility_score'] < 50:
            suggestions.append("元素当前不可见，定位可能不稳定")
        
        # 检查元素是否可用
        if stability_result['enabled_score'] < 50:
            suggestions.append("元素当前不可用，定位可能不稳定")
        
        # 检查总评分
        if stability_result['score'] < 60:
            suggestions.append("定位稳定性较低，建议使用混合定位策略")
        
        return suggestions
    
    def get_stability_level(self, score: int) -> str:
        """获取稳定性级别
        
        Args:
            score: 稳定性评分
            
        Returns:
            稳定性级别
        """
        if score >= 90:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 50:
            return "一般"
        elif score >= 30:
            return "较差"
        else:
            return "很差"
    
    def get_optimization_priority(self, suggestions: list) -> str:
        """获取优化优先级
        
        Args:
            suggestions: 优化建议列表
            
        Returns:
            优化优先级
        """
        if not suggestions:
            return "低"
        
        # 检查是否有严重问题
        for suggestion in suggestions:
            if any(keyword in suggestion for keyword in ["动态生成", "不可见", "不可用", "稳定性较低"]):
                return "高"
        
        return "中"


# 全局稳定性分析器实例
stability_analyzer = StabilityAnalyzer()