#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StabilityAnalyzer类的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from core.stability_analyzer import StabilityAnalyzer
from core.element import Element


def test_stability_analyzer_creation():
    """测试StabilityAnalyzer实例创建"""
    analyzer = StabilityAnalyzer()
    assert analyzer is not None


def test_calculate_stability_score():
    """测试计算稳定性评分"""
    analyzer = StabilityAnalyzer()
    
    # 创建具有稳定属性的元素
    stable_element = Element()
    stable_element.automation_id = "unique_id_123"
    stable_element.class_name = "Button"
    stable_element.name = "确定"
    
    # 计算稳定性评分
    result = analyzer.calculate_stability_score(stable_element)
    
    # 验证结果（稳定元素应该有较高分数）
    assert isinstance(result, dict)
    assert "score" in result
    assert result["score"] > 70  # 稳定元素分数应高于70


def test_calculate_stability_score_dynamic():
    """测试计算动态元素的稳定性评分"""
    analyzer = StabilityAnalyzer()
    
    # 创建具有动态属性的元素
    dynamic_element = Element()
    dynamic_element.class_name = "Button"
    dynamic_element.name = "动态按钮_12345"
    
    # 计算稳定性评分
    result = analyzer.calculate_stability_score(dynamic_element)
    
    # 验证结果（动态元素分数较低）
    assert isinstance(result, dict)
    assert "score" in result
    assert result["score"] < 150  # 动态元素分数应低于150


def test_calculate_stability_score_low_info():
    """测试计算信息较少元素的稳定性评分"""
    analyzer = StabilityAnalyzer()
    
    # 创建只有基本属性的元素
    low_info_element = Element()
    low_info_element.class_name = "Button"
    
    # 计算稳定性评分
    result = analyzer.calculate_stability_score(low_info_element)
    
    # 验证结果（信息较少元素分数较低）
    assert isinstance(result, dict)
    assert "score" in result
    assert result["score"] > 80  # 信息少的元素分数应高于80（由于class_name权重较高）


def test_get_stability_level():
    """测试获取稳定性级别"""
    analyzer = StabilityAnalyzer()
    
    # 测试不同分数的稳定性级别
    assert analyzer.get_stability_level(95) == "优秀"
    assert analyzer.get_stability_level(80) == "良好"
    assert analyzer.get_stability_level(60) == "一般"
    assert analyzer.get_stability_level(40) == "较差"
    assert analyzer.get_stability_level(20) == "很差"


def test_get_optimization_priority():
    """测试获取优化优先级"""
    analyzer = StabilityAnalyzer()
    
    # 测试不同建议的优化优先级
    high_priority_suggestions = ["元素名称可能是动态生成的", "元素层级较深"]
    assert analyzer.get_optimization_priority(high_priority_suggestions) == "高"
    
    low_priority_suggestions = []
    assert analyzer.get_optimization_priority(low_priority_suggestions) == "低"


def test_calculate_stability_score_with_suggestions():
    """测试计算稳定性评分并生成建议"""
    analyzer = StabilityAnalyzer()
    
    # 创建低稳定性元素
    unstable_element = Element()
    unstable_element.class_name = "Button"
    unstable_element.name = "动态按钮_12345"
    
    # 计算稳定性评分
    result = analyzer.calculate_stability_score(unstable_element)
    
    # 验证结果
    assert isinstance(result, dict)
    assert "suggestions" in result
    assert isinstance(result["suggestions"], list)
    assert len(result["suggestions"]) > 0


def test_calculate_attribute_score():
    """测试计算属性评分"""
    analyzer = StabilityAnalyzer()
    
    # 创建具有稳定属性的元素
    stable_element = Element()
    stable_element.automation_id = "unique_id_123"
    stable_element.class_name = "Button"
    stable_element.name = "确定"
    
    # 测试属性评分计算
    result = analyzer.calculate_stability_score(stable_element)
    assert "attribute_scores" in result
    assert isinstance(result["attribute_scores"], dict)
    assert result["attribute_scores"]["automation_id"] == 100  # automation_id 应为满分


def test_calculate_depth_score():
    """测试计算层级深度评分"""
    analyzer = StabilityAnalyzer()
    
    # 测试不同层级的评分
    result = analyzer.calculate_stability_score(Element(), "Window > Button")
    assert result["depth_score"] == 100  # 层级浅，分数高
    
    deep_path = "Window > Group > Panel > Group > Button > Text > Link"
    result = analyzer.calculate_stability_score(Element(), deep_path)
    assert result["depth_score"] == 60  # 层级深，分数应为60


def test_calculate_visibility_score():
    """测试计算可见性评分"""
    analyzer = StabilityAnalyzer()
    
    # 测试可见元素
    visible_element = Element()
    visible_element.is_visible = True
    result = analyzer.calculate_stability_score(visible_element)
    assert result["visibility_score"] == 100
    
    # 测试不可见元素
    invisible_element = Element()
    invisible_element.is_visible = False
    result = analyzer.calculate_stability_score(invisible_element)
    assert result["visibility_score"] == 30