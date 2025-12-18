#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygetwindow as gw
import win32gui
import win32con
import win32process


class WindowUtils:
    """窗口管理工具类"""

    @staticmethod
    def get_all_windows():
        """获取所有可见窗口"""
        return gw.getAllWindows()
    
    @staticmethod
    def get_window_by_title(title, exact_match=False):
        """根据标题获取窗口
        
        Args:
            title: 窗口标题
            exact_match: 是否精确匹配
            
        Returns:
            匹配的窗口对象，没有找到返回None
        """
        if exact_match:
            return gw.getWindowsWithTitle(title)[0] if gw.getWindowsWithTitle(title) else None
        else:
            for window in gw.getAllWindows():
                if title in window.title:
                    return window
            return None
    
    @staticmethod
    def get_windows_by_pid(pid):
        """根据进程ID获取窗口，包括可见和最小化窗口
        
        Args:
            pid: 进程ID
            
        Returns:
            匹配的窗口列表
        """
        result = []
        
        def enum_windows_callback(hwnd, windows):
            # 获取窗口进程ID
            window_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            if window_pid == pid:
                title = win32gui.GetWindowText(hwnd)
                # 不管窗口是否可见，都添加到列表中
                is_visible = win32gui.IsWindowVisible(hwnd)
                is_minimized = win32gui.IsIconic(hwnd)
                is_enabled = win32gui.IsWindowEnabled(hwnd)
                
                # 创建一个简单的窗口对象，包含必要的属性
                window_obj = type('Window', (), {
                    'hwnd': hwnd,
                    'title': title,
                    'pid': pid,
                    'is_visible': is_visible,
                    'is_minimized': is_minimized,
                    'is_enabled': is_enabled
                })()
                windows.append(window_obj)
            return True
        
        win32gui.EnumWindows(enum_windows_callback, result)
        return result
    
    @staticmethod
    def is_window_minimized(hwnd):
        """检查窗口是否最小化
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            True if window is minimized, False otherwise
        """
        return win32gui.IsIconic(hwnd)
    
    @staticmethod
    def restore_window(hwnd):
        """恢复最小化的窗口
        
        Args:
            hwnd: 窗口句柄
        """
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    
    @staticmethod
    def get_window_style(hwnd):
        """获取窗口样式
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            窗口样式值
        """
        return win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    
    @staticmethod
    def is_window_transparent(hwnd):
        """检查窗口是否透明
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            True if window is transparent, False otherwise
        """
        try:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            return style & win32con.WS_EX_LAYERED == win32con.WS_EX_LAYERED
        except Exception:
            return False
    
    @staticmethod
    def get_window_rect(window):
        """获取窗口矩形区域
        
        Args:
            window: 窗口对象或句柄
            
        Returns:
            窗口矩形元组 (left, top, right, bottom)
        """
        if hasattr(window, 'hwnd'):
            hwnd = window.hwnd
        elif isinstance(window, int):
            hwnd = window
        else:
            return None
        
        return win32gui.GetWindowRect(hwnd)
    
    @staticmethod
    def activate_window(window):
        """激活窗口
        
        Args:
            window: 窗口对象或句柄
        """
        if hasattr(window, 'activate'):
            window.activate()
        elif isinstance(window, int):
            win32gui.ShowWindow(window, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(window)
    
    @staticmethod
    def get_window_title(window):
        """获取窗口标题
        
        Args:
            window: 窗口对象或句柄
            
        Returns:
            窗口标题字符串
        """
        if hasattr(window, 'title'):
            return window.title
        elif isinstance(window, int):
            return win32gui.GetWindowText(window)
        return ""
    
    @staticmethod
    def get_window_pid(window):
        """获取窗口所属进程ID
        
        Args:
            window: 窗口对象或句柄
            
        Returns:
            进程ID
        """
        if hasattr(window, 'pid'):
            return window.pid
        elif isinstance(window, int):
            return win32process.GetWindowThreadProcessId(window)[1]
        return None
