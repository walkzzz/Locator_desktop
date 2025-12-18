#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime


class HistoryManager:
    """定位历史记录管理器"""

    def __init__(self, history_file='history.json'):
        """初始化历史记录管理器
        
        Args:
            history_file: 历史记录文件路径
        """
        self.history_file = os.path.join(os.path.dirname(__file__), '..', 'data', history_file)
        self._ensure_data_directory()
        self.history = self._load_history()
    
    def _ensure_data_directory(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.history_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_history(self):
        """加载历史记录
        
        Returns:
            历史记录列表
        """
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            return []
    
    def _save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def add_record(self, element, method, code, result):
        """添加历史记录
        
        Args:
            element: 元素对象
            method: 定位方法
            code: 生成的代码
            result: 定位结果
        """
        # 构建历史记录
        record = {
            'id': len(self.history) + 1,
            'timestamp': datetime.now().isoformat(),
            'application': element.name or 'Unknown',
            'element_type': element.element_type,
            'element_name': element.name,
            'automation_id': element.automation_id,
            'class_name': element.class_name,
            'method': method,
            'code': code,
            'result': result,
            'coordinates': {
                'x': element.x,
                'y': element.y,
                'width': element.width,
                'height': element.height
            }
        }
        
        # 添加到历史记录列表
        self.history.insert(0, record)  # 最新的记录放在最前面
        
        # 限制历史记录数量，最多保存100条
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        # 保存到文件
        self._save_history()
    
    def get_all_records(self):
        """获取所有历史记录
        
        Returns:
            历史记录列表
        """
        return self.history
    
    def search_records(self, keyword):
        """搜索历史记录
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的历史记录列表
        """
        if not keyword:
            return self.history
        
        keyword = keyword.lower()
        return [record for record in self.history if 
                keyword in record['application'].lower() or 
                keyword in record['element_type'].lower() or 
                keyword in (record['element_name'] or '').lower() or 
                keyword in (record['automation_id'] or '').lower()]
    
    def delete_record(self, record_id):
        """删除历史记录
        
        Args:
            record_id: 记录ID
        """
        self.history = [record for record in self.history if record['id'] != record_id]
        self._save_history()
    
    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self._save_history()
    
    def get_record_by_id(self, record_id):
        """根据ID获取历史记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            匹配的历史记录或None
        """
        for record in self.history:
            if record['id'] == record_id:
                return record
        return None
