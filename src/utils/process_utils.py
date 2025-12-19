#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil


class ProcessUtils:
    """进程管理工具类"""

    @staticmethod
    def get_running_processes():
        """获取所有正在运行的进程
        
        Returns:
            正在运行的进程列表，每个进程包含name和pid属性
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # 创建一个简单的进程对象，包含必要的属性
                process_obj = type('Process', (), {
                    'pid': proc.info['pid'],
                    'name': proc.info['name']
                })()
                processes.append(process_obj)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes
    
    @staticmethod
    def get_process_by_pid(pid):
        """根据进程ID获取进程信息
        
        Args:
            pid: 进程ID
            
        Returns:
            进程对象，没有找到返回None
        """
        try:
            proc = psutil.Process(pid)
            # 创建一个简单的进程对象，包含必要的属性
            process_obj = type('Process', (), {
                'pid': proc.pid,
                'name': proc.name(),
                'exe': proc.exe()
            })()
            return process_obj
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    @staticmethod
    def get_process_by_name(name):
        """根据进程名获取进程列表
        
        Args:
            name: 进程名
            
        Returns:
            匹配的进程列表
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == name:
                    process_obj = type('Process', (), {
                        'pid': proc.info['pid'],
                        'name': proc.info['name']
                    })()
                    processes.append(process_obj)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes
    
    @staticmethod
    def is_process_running(pid):
        """检查进程是否正在运行
        
        Args:
            pid: 进程ID
            
        Returns:
            进程是否正在运行
        """
        try:
            proc = psutil.Process(pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
    
    @staticmethod
    def get_process_exe(pid):
        """获取进程可执行文件路径
        
        Args:
            pid: 进程ID
            
        Returns:
            进程可执行文件路径，获取失败返回None
        """
        try:
            proc = psutil.Process(pid)
            return proc.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    @staticmethod
    def start_process(exe_path, args=None):
        """启动进程
        
        Args:
            exe_path: 可执行文件路径
            args: 命令行参数列表
            
        Returns:
            启动的进程对象，失败返回None
        """
        import subprocess
        try:
            process = subprocess.Popen([exe_path] + (args or []))
            return process
        except Exception as e:
            print(f"启动进程失败: {e}")
            return None
