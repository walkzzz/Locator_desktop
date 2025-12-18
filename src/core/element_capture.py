#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import win32gui
import win32con
import win32api
import pywinauto
import uiautomation as auto

from .element import Element


class ElementCapture:
    """元素捕获核心逻辑类"""

    def __init__(self):
        self.capturing = False
        self.last_captured_element = None
    
    def capture_element(self):
        """捕获元素
        
        Returns:
            捕获到的元素对象，没有捕获到返回None
        """
        print("开始捕获元素，请将鼠标移动到目标元素上，按下Ctrl键确认...")
        
        self.capturing = True
        captured_element = None
        
        try:
            # 等待用户按下Ctrl键
            while self.capturing:
                # 获取当前鼠标位置
                x, y = win32api.GetCursorPos()
                
                # 获取鼠标下的窗口
                hwnd = win32gui.WindowFromPoint((x, y))
                if hwnd:
                    # 使用pywinauto获取元素
                    element = self._get_element_by_coordinate(hwnd, x, y)
                    if element:
                        self.last_captured_element = element
                        print(f"捕获到元素: {element}")
                
                # 检查是否按下了Ctrl键
                if win32api.GetKeyState(win32con.VK_CONTROL) < 0:
                    captured_element = self.last_captured_element
                    break
                
                # 短暂延迟，减少CPU占用
                time.sleep(0.1)
        except Exception as e:
            print(f"捕获元素时发生错误: {e}")
        finally:
            self.capturing = False
        
        return captured_element
    
    def _get_element_by_coordinate(self, hwnd, x, y):
        """根据坐标获取元素，支持最小化窗口
        
        Args:
            hwnd: 窗口句柄
            x: 鼠标x坐标
            y: 鼠标y坐标
            
        Returns:
            元素对象，获取失败返回None
        """
        try:
            from utils.window_utils import WindowUtils
            
            # 检查窗口是否最小化
            is_minimized = WindowUtils.is_window_minimized(hwnd)
            restore_needed = False
            
            if is_minimized:
                # 恢复最小化窗口
                WindowUtils.restore_window(hwnd)
                restore_needed = True
            
            try:
                # 获取窗口所属的应用类型
                app_type = self._detect_application_type(hwnd)
                
                # 根据应用类型选择不同的定位策略
                if app_type == 'Qt':
                    # Qt应用优先使用objectName属性
                    return self._get_element_by_coordinate_with_backend(hwnd, x, y, backend='win32')
                elif app_type in ['MFC', 'WinForms']:
                    # MFC和WinForms应用使用默认backend
                    return self._get_element_by_coordinate_with_backend(hwnd, x, y, backend='win32')
                elif app_type == 'WPF':
                    # WPF应用使用uia backend
                    return self._get_element_by_coordinate_with_backend(hwnd, x, y, backend='uia')
                else:
                    # 自动检测最佳backend
                    # 先尝试uia backend
                    element = self._get_element_by_coordinate_with_backend(hwnd, x, y, backend='uia')
                    if element:
                        return element
                    # 再尝试win32 backend
                    return self._get_element_by_coordinate_with_backend(hwnd, x, y, backend='win32')
            finally:
                # 如果需要，恢复窗口状态
                if restore_needed:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        except Exception as e:
            print(f"使用pywinauto获取元素失败: {e}")
        
        return None
    
    def _get_element_by_coordinate_with_backend(self, hwnd, x, y, backend='uia'):
        """使用指定backend根据坐标获取元素
        
        Args:
            hwnd: 窗口句柄
            x: 鼠标x坐标
            y: 鼠标y坐标
            backend: 使用的backend，可选值: 'uia', 'win32'
            
        Returns:
            元素对象，获取失败返回None
        """
        try:
            # 使用pywinauto获取元素
            app = pywinauto.Application(backend=backend).connect(handle=hwnd)
            window = app.window(handle=hwnd)
            element = window.from_point((x, y))
            if element:
                return self._convert_pywinauto_to_element(element)
        except Exception as e:
            print(f"使用{backend} backend获取元素失败: {e}")
        
        return None
    
    def _detect_application_type(self, hwnd):
        """检测应用类型
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            应用类型字符串，如: 'MFC', 'WinForms', 'WPF', 'Qt', 'Unknown'
        """
        try:
            # 获取窗口类名
            class_name = win32gui.GetClassName(hwnd)
            
            # 根据类名判断应用类型
            if 'Qt5' in class_name or 'Qt6' in class_name or 'QWidget' in class_name:
                return 'Qt'
            elif 'WindowsForms' in class_name or 'Control' in class_name:
                return 'WinForms'
            elif 'HwndWrapper' in class_name:
                return 'WPF'
            elif 'Afx' in class_name or 'Mfc' in class_name:
                return 'MFC'
            else:
                return 'Unknown'
        except Exception as e:
            print(f"检测应用类型失败: {e}")
            return 'Unknown'
    
    def _convert_to_element(self, automation_element):
        """将uiautomation元素转换为自定义Element对象
        
        Args:
            automation_element: uiautomation元素对象
            
        Returns:
            自定义Element对象
        """
        element = Element()
        
        # 基本信息
        element.element_type = automation_element.ControlTypeName
        element.control_type = automation_element.ControlType
        element.class_name = automation_element.ClassName
        element.automation_id = automation_element.AutomationId
        
        # 元素名称和文本
        element.name = automation_element.Name
        element.text = automation_element.Name
        
        # 元素位置和尺寸
        rect = automation_element.BoundingRectangle
        element.x = rect.left
        element.y = rect.top
        element.width = rect.right - rect.left
        element.height = rect.bottom - rect.top
        
        # 元素状态
        element.is_enabled = automation_element.IsEnabled
        element.is_visible = automation_element.IsOffscreen == False
        
        # 其他属性
        element.process_id = automation_element.ProcessId
        element.window_handle = automation_element.NativeWindowHandle
        
        return element
    
    def _convert_pywinauto_to_element(self, pywinauto_element):
        """将pywinauto元素转换为自定义Element对象
        
        Args:
            pywinauto_element: pywinauto元素对象
            
        Returns:
            自定义Element对象
        """
        element = Element()
        
        # 基本信息
        element.element_type = pywinauto_element.element_info.control_type
        element.control_type = pywinauto_element.element_info.control_type
        element.class_name = pywinauto_element.element_info.class_name
        element.automation_id = pywinauto_element.element_info.automation_id
        
        # 元素名称和文本
        element.name = pywinauto_element.element_info.name
        element.text = pywinauto_element.element_info.name
        
        # 元素位置和尺寸
        rect = pywinauto_element.element_info.rectangle
        element.x = rect.left
        element.y = rect.top
        element.width = rect.width()
        element.height = rect.height()
        
        # 元素状态
        element.is_enabled = pywinauto_element.is_enabled()
        element.is_visible = pywinauto_element.is_visible()
        
        # 其他属性
        element.process_id = pywinauto_element.element_info.process_id
        element.window_handle = pywinauto_element.element_info.handle
        
        return element
    
    def test_element_location(self, element):
        """测试元素定位是否有效
        
        Args:
            element: 元素对象
            
        Returns:
            定位是否成功
        """
        try:
            if not element or not element.window_handle:
                return False
            
            # 检测应用类型
            app_type = self._detect_application_type(element.window_handle)
            
            # 根据应用类型选择合适的backend
            if app_type == 'Qt' or app_type in ['MFC', 'WinForms']:
                backends = ['win32', 'uia']  # 优先尝试win32 backend
            elif app_type == 'WPF':
                backends = ['uia', 'win32']  # 优先尝试uia backend
            else:
                backends = ['uia', 'win32']  # 默认先尝试uia backend
            
            # 尝试不同的backend
            for backend in backends:
                try:
                    # 使用pywinauto测试定位
                    app = pywinauto.Application(backend=backend).connect(handle=element.window_handle)
                    window = app.window(handle=element.window_handle)
                    
                    # 根据元素属性构建定位条件
                    conditions = {}
                    
                    if element.automation_id:
                        conditions['auto_id' if backend == 'uia' else 'id'] = element.automation_id
                        try:
                            found_element = window.child_window(**conditions)
                            if found_element.exists():
                                return True
                        except Exception as e:
                            print(f"使用{backend} backend根据automation_id查找失败: {e}")
                    
                    # 根据名称查找
                    if element.name:
                        conditions = {'name': element.name}
                        try:
                            found_element = window.child_window(**conditions)
                            if found_element.exists():
                                return True
                        except Exception as e:
                            print(f"使用{backend} backend根据名称查找失败: {e}")
                    
                    # 根据类名查找
                    if element.class_name:
                        conditions = {'class_name': element.class_name}
                        try:
                            found_element = window.child_window(**conditions)
                            if found_element.exists():
                                return True
                        except Exception as e:
                            print(f"使用{backend} backend根据类名查找失败: {e}")
                    
                except Exception as e:
                    print(f"使用{backend} backend测试元素定位失败: {e}")
                    continue
            
            return False
        except Exception as e:
            print(f"测试元素定位失败: {e}")
            return False
    
    def __init__(self):
        self.capturing = False
        self.last_captured_element = None
        self.template_cache = {}  # 模板缓存
        self.screenshot_cache = None  # 截图缓存
        self.screenshot_time = 0  # 截图时间
    
    def capture_element_by_image(self, image_path, confidence=0.8):
        """通过图像识别捕获元素
        
        Args:
            image_path: 图像文件路径
            confidence: 识别置信度
            
        Returns:
            元素对象，识别失败返回None
        """
        try:
            import cv2
            import numpy as np
            from PIL import ImageGrab
            import time
            
            # 检查模板缓存
            if image_path in self.template_cache:
                # 使用缓存的模板
                template = self.template_cache[image_path]
            else:
                # 读取模板图像
                template = cv2.imread(image_path)
                if template is None:
                    print("无法读取模板图像")
                    return None
                
                # 图像预处理：裁剪边缘冗余区域、调整对比度
                template = self._preprocess_image(template)
                
                # 缓存模板
                self.template_cache[image_path] = template
            
            # 获取屏幕截图，带缓存机制
            current_time = time.time()
            if self.screenshot_cache is None or current_time - self.screenshot_time > 0.5:
                # 超过0.5秒，重新截图
                screenshot = ImageGrab.grab()
                self.screenshot_cache = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                self.screenshot_time = current_time
            
            # 使用缓存的截图
            screenshot = self.screenshot_cache
            
            # 多级缩放匹配
            max_val, max_loc = self._multi_scale_match(screenshot, template)
            
            if max_val >= confidence:
                # 创建元素对象
                element = Element()
                element.element_type = "ImageMatched"
                element.x = max_loc[0]
                element.y = max_loc[1]
                element.width = template.shape[1]
                element.height = template.shape[0]
                element.name = f"ImageMatched_{max_val:.2f}"
                
                return element
            else:
                print(f"图像匹配置信度不足: {max_val:.2f} < {confidence}")
                return None
        except Exception as e:
            print(f"图像识别捕获元素失败: {e}")
            return None
    
    def _preprocess_image(self, image):
        """图像预处理
        
        Args:
            image: 输入图像
            
        Returns:
            预处理后的图像
        """
        import cv2
        import numpy as np
        
        # 1. 裁剪边缘冗余区域
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        coords = cv2.findNonZero(thresh)
        x, y, w, h = cv2.boundingRect(coords)
        cropped = image[y:y+h, x:x+w]
        
        # 2. 调整对比度
        alpha = 1.2  # 对比度因子
        beta = 0     # 亮度偏移
        adjusted = cv2.convertScaleAbs(cropped, alpha=alpha, beta=beta)
        
        return adjusted
    
    def _multi_scale_match(self, screenshot, template):
        """多级缩放匹配
        
        Args:
            screenshot: 截图图像
            template: 模板图像
            
        Returns:
            (最大匹配值, 最大匹配位置)
        """
        import cv2
        import numpy as np
        
        # 缩放因子范围
        scales = np.linspace(0.8, 1.2, 5)  # 5个缩放级别，从0.8到1.2
        
        max_val = 0
        max_loc = (0, 0)
        
        # 先使用低分辨率快速粗匹配
        small_screenshot = cv2.resize(screenshot, (0, 0), fx=0.5, fy=0.5)
        small_template = cv2.resize(template, (0, 0), fx=0.5, fy=0.5)
        
        # 快速粗匹配
        result = cv2.matchTemplate(small_screenshot, small_template, cv2.TM_CCOEFF_NORMED)
        _, temp_max_val, _, temp_max_loc = cv2.minMaxLoc(result)
        
        if temp_max_val > max_val:
            max_val = temp_max_val
            max_loc = (temp_max_loc[0] * 2, temp_max_loc[1] * 2)  # 恢复原始尺寸
        
        # 对候选区域进行高分辨率精确匹配
        h, w = template.shape[:2]
        search_region = screenshot[max(0, max_loc[1]-h//2):max_loc[1]+h*2, max(0, max_loc[0]-w//2):max_loc[0]+w*2]
        
        for scale in scales:
            # 缩放模板
            scaled_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            sh, sw = scaled_template.shape[:2]
            
            if sh > search_region.shape[0] or sw > search_region.shape[1]:
                continue
            
            # 模板匹配
            result = cv2.matchTemplate(search_region, scaled_template, cv2.TM_CCOEFF_NORMED)
            _, temp_max_val, _, temp_max_loc = cv2.minMaxLoc(result)
            
            if temp_max_val > max_val:
                max_val = temp_max_val
                # 转换为原始图像坐标
                max_loc = (max_loc[0]-w//2+temp_max_loc[0], max_loc[1]-h//2+temp_max_loc[1])
        
        return max_val, max_loc
    
    def batch_capture_element(self):
        """批量捕获元素，支持框选区域内的多个元素
        
        Returns:
            捕获到的元素列表，或None
        """
        print("开始批量捕获元素，请拖拽鼠标框选目标区域...")
        
        # 使用pygetwindow获取屏幕尺寸
        import pygetwindow as gw
        screen_width, screen_height = gw.getScreenSize()
        
        # 记录鼠标按下和释放的位置
        start_x, start_y = None, None
        end_x, end_y = None, None
        
        # 绘制矩形框选
        def draw_selection_rectangle(canvas, start, end):
            """绘制选择矩形"""
            import win32gui
            import win32con
            
            # 获取设备上下文
            hdc = win32gui.GetDC(0)
            
            # 创建画笔和画刷
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32gui.RGB(255, 0, 0))
            brush = win32gui.CreateSolidBrush(win32gui.RGB(255, 0, 0))
            
            # 选择画笔
            win32gui.SelectObject(hdc, pen)
            win32gui.SelectObject(hdc, brush)
            
            # 绘制半透明矩形
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
            win32gui.SetROP2(hdc, win32con.R2_NOTXORPEN)
            
            # 计算矩形坐标
            left = min(start[0], end[0])
            top = min(start[1], end[1])
            right = max(start[0], end[0])
            bottom = max(start[1], end[1])
            
            # 绘制矩形
            win32gui.Rectangle(hdc, left, top, right, bottom)
            
            # 清理资源
            win32gui.DeleteObject(pen)
            win32gui.DeleteObject(brush)
            win32gui.ReleaseDC(0, hdc)
        
        try:
            import win32api
            import win32con
            
            # 等待用户按下鼠标左键
            print("按下鼠标左键开始框选...")
            while True:
                if win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                    start_x, start_y = win32api.GetCursorPos()
                    break
                time.sleep(0.01)
            
            # 记录初始位置
            last_x, last_y = start_x, start_y
            
            # 等待用户释放鼠标左键
            print("拖拽鼠标框选区域...")
            while True:
                current_x, current_y = win32api.GetCursorPos()
                
                # 如果鼠标位置变化，绘制矩形
                if current_x != last_x or current_y != last_y:
                    # 清除上次绘制的矩形
                    draw_selection_rectangle(None, (start_x, start_y), (last_x, last_y))
                    # 绘制新的矩形
                    draw_selection_rectangle(None, (start_x, start_y), (current_x, current_y))
                    last_x, last_y = current_x, current_y
                
                # 检查是否释放鼠标左键
                if win32api.GetKeyState(win32con.VK_LBUTTON) >= 0:
                    end_x, end_y = current_x, current_y
                    break
                
                time.sleep(0.01)
            
            # 清除最终的矩形
            draw_selection_rectangle(None, (start_x, start_y), (end_x, end_y))
            
            # 计算框选区域
            left = min(start_x, end_x)
            top = min(start_y, end_y)
            right = max(start_x, end_x)
            bottom = max(start_y, end_y)
            
            print(f"框选区域: ({left}, {top}) - ({right}, {bottom})")
            
            # 获取框选区域内的所有元素
            return self._get_elements_in_region(left, top, right, bottom)
            
        except Exception as e:
            print(f"批量捕获元素时发生错误: {e}")
            return None
        finally:
            self.capturing = False
    
    def _get_elements_in_region(self, left, top, right, bottom):
        """获取指定区域内的所有元素
        
        Args:
            left: 区域左上角x坐标
            top: 区域左上角y坐标
            right: 区域右下角x坐标
            bottom: 区域右下角y坐标
            
        Returns:
            区域内的元素列表
        """
        elements = []
        
        try:
            # 获取当前鼠标下的窗口
            mouse_x, mouse_y = win32api.GetCursorPos()
            hwnd = win32gui.WindowFromPoint((mouse_x, mouse_y))
            
            if hwnd:
                # 使用pywinauto获取窗口内的所有元素
                app = pywinauto.Application(backend='uia').connect(handle=hwnd)
                window = app.window(handle=hwnd)
                
                # 获取所有子元素
                all_elements = window.descendants()
                
                for pywinauto_element in all_elements:
                    # 获取元素的位置和尺寸
                    rect = pywinauto_element.rectangle()
                    element_left = rect.left
                    element_top = rect.top
                    element_right = rect.right
                    element_bottom = rect.bottom
                    
                    # 检查元素是否在区域内
                    if (element_right >= left and element_left <= right and
                        element_bottom >= top and element_top <= bottom):
                        # 转换为自定义Element对象
                        element = self._convert_pywinauto_to_element(pywinauto_element)
                        elements.append(element)
        except Exception as e:
            print(f"获取区域内元素失败: {e}")
        
        print(f"在区域内找到 {len(elements)} 个元素")
        return elements
