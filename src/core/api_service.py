#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API服务模块
暴露核心功能API，支持其他工具通过HTTP或本地调用集成Locator_desktop的能力
"""

import threading
import json
from flask import Flask, request, jsonify


class APIService:
    """API服务类"""
    
    def __init__(self, app):
        """初始化API服务
        
        Args:
            app: 主应用实例
        """
        self.app = app
        self.flask_app = Flask(__name__)
        self.server_thread = None
        self.is_running = False
        self.port = 5000
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册API路由"""
        @self.flask_app.route('/api/v1/capture_element', methods=['POST'])
        def capture_element():
            """捕获元素API"""
            try:
                element = self.app.element_capture.capture_element()
                if element:
                    return jsonify({
                        "success": True,
                        "data": {
                            "element_id": element.element_id,
                            "element_type": element.element_type,
                            "name": element.name,
                            "automation_id": element.automation_id,
                            "class_name": element.class_name,
                            "x": element.x,
                            "y": element.y,
                            "width": element.width,
                            "height": element.height,
                            "process_id": element.process_id,
                            "window_handle": element.window_handle
                        }
                    })
                else:
                    return jsonify({"success": False, "error": "未捕获到元素"}), 400
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.flask_app.route('/api/v1/generate_code', methods=['POST'])
        def generate_code():
            """生成定位代码API"""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "请求数据不能为空"}), 400
                
                # 获取请求参数
                element_data = data.get('element')
                method = data.get('method', 'auto')
                
                if not element_data:
                    return jsonify({"success": False, "error": "元素数据不能为空"}), 400
                
                # 转换为元素对象
                element = self._create_element_from_data(element_data)
                
                # 生成代码
                code = self.app.code_generator.generate_code_by_method(element, method)
                
                return jsonify({
                    "success": True,
                    "data": {
                        "code": code,
                        "method": method
                    }
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.flask_app.route('/api/v1/generate_complete_script', methods=['POST'])
        def generate_complete_script():
            """生成完整可执行脚本API"""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "请求数据不能为空"}), 400
                
                # 获取请求参数
                element_data = data.get('element')
                method = data.get('method', 'auto')
                
                if not element_data:
                    return jsonify({"success": False, "error": "元素数据不能为空"}), 400
                
                # 转换为元素对象
                element = self._create_element_from_data(element_data)
                
                # 生成完整脚本
                script = self.app.code_generator.generate_complete_script(element, method)
                
                return jsonify({
                    "success": True,
                    "data": {
                        "script": script,
                        "method": method
                    }
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.flask_app.route('/api/v1/test_location', methods=['POST'])
        def test_location():
            """测试定位API"""
            try:
                data = request.json
                if not data:
                    return jsonify({"success": False, "error": "请求数据不能为空"}), 400
                
                # 获取请求参数
                element_data = data.get('element')
                
                if not element_data:
                    return jsonify({"success": False, "error": "元素数据不能为空"}), 400
                
                # 转换为元素对象
                element = self._create_element_from_data(element_data)
                
                # 测试定位
                result = self.app.element_capture.test_element_location(element)
                
                return jsonify({
                    "success": True,
                    "data": {
                        "result": result
                    }
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.flask_app.route('/api/v1/get_window_list', methods=['GET'])
        def get_window_list():
            """获取窗口列表API"""
            try:
                # 获取所有窗口
                windows = self.app.window_utils.get_all_windows()
                
                # 转换为字典列表
                window_list = []
                for window in windows:
                    window_list.append({
                        "title": window.title,
                        "hwnd": window.hwnd if hasattr(window, 'hwnd') else None,
                        "pid": window.pid if hasattr(window, 'pid') else None,
                        "is_visible": window.is_visible if hasattr(window, 'is_visible') else None
                    })
                
                return jsonify({
                    "success": True,
                    "data": {
                        "windows": window_list
                    }
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        
        @self.flask_app.route('/api/v1/ping', methods=['GET'])
        def ping():
            """心跳检测API"""
            return jsonify({
                "success": True,
                "data": {
                    "message": "pong",
                    "version": "1.0.0"
                }
            })
    
    def _create_element_from_data(self, element_data):
        """从数据创建元素对象
        
        Args:
            element_data: 元素数据字典
            
        Returns:
            元素对象
        """
        from core.element import Element
        
        element = Element()
        element.element_id = element_data.get('element_id')
        element.element_type = element_data.get('element_type')
        element.name = element_data.get('name')
        element.automation_id = element_data.get('automation_id')
        element.class_name = element_data.get('class_name')
        element.x = element_data.get('x')
        element.y = element_data.get('y')
        element.width = element_data.get('width')
        element.height = element_data.get('height')
        element.process_id = element_data.get('process_id')
        element.window_handle = element_data.get('window_handle')
        
        return element
    
    def start(self, port=5000):
        """启动API服务
        
        Args:
            port: 服务端口
        """
        if not self.is_running:
            self.port = port
            self.server_thread = threading.Thread(
                target=self.flask_app.run, 
                kwargs={
                    'host': '0.0.0.0', 
                    'port': port,
                    'debug': False,
                    'use_reloader': False
                },
                daemon=True
            )
            self.server_thread.start()
            self.is_running = True
            print(f"API服务已启动，端口: {port}")
    
    def stop(self):
        """停止API服务"""
        if self.is_running:
            # Flask内置服务器不支持优雅关闭，这里只是标记状态
            self.is_running = False
            print("API服务已停止")
    
    def is_running(self):
        """检查API服务是否正在运行
        
        Returns:
            True if running, False otherwise
        """
        return self.is_running
    
    def get_api_info(self):
        """获取API服务信息
        
        Returns:
            包含API服务信息的字典
        """
        return {
            "running": self.is_running,
            "port": self.port,
            "base_url": f"http://localhost:{self.port}",
            "endpoints": [
                "/api/v1/ping",
                "/api/v1/capture_element",
                "/api/v1/generate_code",
                "/api/v1/generate_complete_script",
                "/api/v1/test_location",
                "/api/v1/get_window_list"
            ]
        }
