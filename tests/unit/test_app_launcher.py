#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用程序启动和异常处理的单元测试
"""

import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import pytest
from unittest.mock import Mock, patch
import psutil
from utils.process_utils import ProcessUtils


class TestProcessUtils:
    """测试ProcessUtils类的start_process方法"""
    
    def test_start_process_success(self):
        """测试成功启动进程"""
        with patch('subprocess.Popen') as mock_popen:
            # 模拟Popen返回值
            mock_process = Mock()
            mock_popen.return_value = mock_process
            
            # 调用start_process方法
            process = ProcessUtils.start_process('notepad.exe')
            
            # 验证结果
            assert process is not None
            assert process == mock_process
            mock_popen.assert_called_once_with(['notepad.exe'])
    
    def test_start_process_with_args(self):
        """测试带参数启动进程"""
        with patch('subprocess.Popen') as mock_popen:
            # 模拟Popen返回值
            mock_process = Mock()
            mock_popen.return_value = mock_process
            
            # 调用start_process方法，带参数
            process = ProcessUtils.start_process('notepad.exe', ['test.txt'])
            
            # 验证结果
            assert process is not None
            assert process == mock_process
            mock_popen.assert_called_once_with(['notepad.exe', 'test.txt'])
    
    def test_start_process_failure(self):
        """测试启动进程失败"""
        with patch('subprocess.Popen', side_effect=Exception('启动失败')) as mock_popen:
            # 调用start_process方法，预期会失败
            process = ProcessUtils.start_process('invalid_app.exe')
            
            # 验证结果
            assert process is None
            mock_popen.assert_called_once_with(['invalid_app.exe'])
    
    def test_is_process_running(self):
        """测试检查进程是否运行"""
        with patch('psutil.Process') as mock_process_class:
            # 模拟进程正在运行
            mock_process = Mock()
            mock_process.is_running.return_value = True
            mock_process_class.return_value = mock_process
            
            # 调用is_process_running方法
            result = ProcessUtils.is_process_running(1234)
            
            # 验证结果
            assert result is True
            mock_process_class.assert_called_once_with(1234)
            mock_process.is_running.assert_called_once()
    
    def test_is_process_not_running(self):
        """测试检查进程未运行"""
        with patch('psutil.Process', side_effect=psutil.NoSuchProcess(1234)):
            # 调用is_process_running方法，预期进程不存在
            result = ProcessUtils.is_process_running(1234)
            
            # 验证结果
            assert result is False
    
    def test_get_process_exe(self):
        """测试获取进程可执行文件路径"""
        with patch('psutil.Process') as mock_process_class:
            # 模拟进程可执行文件路径
            mock_process = Mock()
            mock_process.exe.return_value = 'C:\\Windows\\System32\\notepad.exe'
            mock_process_class.return_value = mock_process
            
            # 调用get_process_exe方法
            exe_path = ProcessUtils.get_process_exe(1234)
            
            # 验证结果
            assert exe_path == 'C:\\Windows\\System32\\notepad.exe'
            mock_process_class.assert_called_once_with(1234)
            mock_process.exe.assert_called_once()
    
    def test_get_process_exe_access_denied(self):
        """测试获取进程可执行文件路径时权限被拒绝"""
        with patch('psutil.Process', side_effect=psutil.AccessDenied(1234)):
            # 调用get_process_exe方法，预期权限被拒绝
            exe_path = ProcessUtils.get_process_exe(1234)
            
            # 验证结果
            assert exe_path is None


class TestAppPathValidation:
    """测试应用程序路径验证逻辑"""
    
    def test_path_exists(self):
        """测试路径存在验证"""
        # 使用当前文件作为测试路径
        current_file = __file__
        assert os.path.exists(current_file) is True
    
    def test_path_not_exists(self):
        """测试路径不存在验证"""
        invalid_path = 'invalid_path.exe'
        assert os.path.exists(invalid_path) is False
    
    def test_file_is_executable_windows(self):
        """测试Windows可执行文件验证"""
        if os.name == 'nt':
            # 在Windows上测试
            notepad_path = 'C:\\Windows\\System32\\notepad.exe'
            if os.path.exists(notepad_path):
                assert notepad_path.lower().endswith('.exe') is True
    
    def test_file_is_executable_linux(self):
        """测试Linux可执行文件验证"""
        if os.name == 'posix':
            # 在Linux/macOS上测试
            # 使用/bin/ls作为测试文件
            ls_path = '/bin/ls'
            if os.path.exists(ls_path):
                assert os.access(ls_path, os.X_OK) is True
