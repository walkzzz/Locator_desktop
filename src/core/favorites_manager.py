#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime


class FavoritesManager:
    """元素收藏夹管理器"""

    def __init__(self, favorites_file='favorites.json'):
        """初始化收藏夹管理器
        
        Args:
            favorites_file: 收藏夹文件路径
        """
        self.favorites_file = os.path.join(os.path.dirname(__file__), '..', 'data', favorites_file)
        self._ensure_data_directory()
        self.favorites = self._load_favorites()
    
    def _ensure_data_directory(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.favorites_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_favorites(self):
        """加载收藏夹
        
        Returns:
            收藏夹列表
        """
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"加载收藏夹失败: {e}")
            return []
    
    def _save_favorites(self):
        """保存收藏夹"""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存收藏夹失败: {e}")
    
    def add_favorite(self, element, tags=None):
        """添加元素到收藏夹
        
        Args:
            element: 元素对象
            tags: 标签列表
            
        Returns:
            是否添加成功
        """
        # 检查元素是否已存在
        if any(fav['element_id'] == element.element_id for fav in self.favorites):
            return False
        
        # 构建收藏项
        favorite = {
            'id': len(self.favorites) + 1,
            'added_at': datetime.now().isoformat(),
            'element_id': element.element_id,
            'element_type': element.element_type,
            'element_name': element.name,
            'application': element.name or 'Unknown',
            'automation_id': element.automation_id,
            'class_name': element.class_name,
            'tags': tags or [],
            'coordinates': {
                'x': element.x,
                'y': element.y,
                'width': element.width,
                'height': element.height
            }
        }
        
        # 添加到收藏夹
        self.favorites.append(favorite)
        self._save_favorites()
        return True
    
    def remove_favorite(self, favorite_id):
        """从收藏夹移除元素
        
        Args:
            favorite_id: 收藏项ID
        """
        self.favorites = [fav for fav in self.favorites if fav['id'] != favorite_id]
        self._save_favorites()
    
    def get_all_favorites(self):
        """获取所有收藏的元素
        
        Returns:
            收藏夹列表
        """
        return self.favorites
    
    def search_favorites(self, keyword):
        """搜索收藏夹
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的收藏项列表
        """
        if not keyword:
            return self.favorites
        
        keyword = keyword.lower()
        return [fav for fav in self.favorites if 
                keyword in fav['application'].lower() or 
                keyword in fav['element_type'].lower() or 
                keyword in (fav['element_name'] or '').lower() or 
                keyword in (fav['automation_id'] or '').lower() or 
                any(keyword in tag.lower() for tag in fav['tags'])]
    
    def update_favorite_tags(self, favorite_id, tags):
        """更新收藏项的标签
        
        Args:
            favorite_id: 收藏项ID
            tags: 新的标签列表
        """
        for fav in self.favorites:
            if fav['id'] == favorite_id:
                fav['tags'] = tags
                self._save_favorites()
                break
    
    def get_favorite_by_id(self, favorite_id):
        """根据ID获取收藏项
        
        Args:
            favorite_id: 收藏项ID
            
        Returns:
            匹配的收藏项或None
        """
        for fav in self.favorites:
            if fav['id'] == favorite_id:
                return fav
        return None
    
    def get_favorite_by_element_id(self, element_id):
        """根据元素ID获取收藏项
        
        Args:
            element_id: 元素ID
            
        Returns:
            匹配的收藏项或None
        """
        for fav in self.favorites:
            if fav['element_id'] == element_id:
                return fav
        return None
