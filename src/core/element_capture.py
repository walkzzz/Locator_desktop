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
                    if self.last_captured_element:
                        captured_element = self.last_captured_element
                        print(f"确认捕获元素: {captured_element}")
                    else:
                        print("未捕获到任何元素，请确保鼠标移动到了有效元素上")
                    break
                
                # 短暂延迟，减少CPU占用
                time.sleep(0.1)
        except Exception as e:
            print(f"捕获元素时发生错误: {type(e).__name__}: {str(e)}")
            print(f"错误解决方案: 1. 确保目标应用正在运行 2. 检查应用是否具有UIA支持 3. 尝试使用其他捕获方式")
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
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"使用pywinauto获取元素失败: {error_type}: {error_msg}")
            print(f"错误解决方案: ")
            print(f"1. 检查窗口是否正常显示，未被其他窗口遮挡")
            print(f"2. 确保应用程序正在正常运行")
            print(f"3. 尝试手动激活目标窗口后再次捕获")
            print(f"4. 对于特殊应用，尝试使用图像识别捕获方式")
        
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
            if not element:
                print("测试定位失败: 无效的元素对象")
                return False
            
            if not element.window_handle:
                print("测试定位失败: 元素缺少窗口句柄")
                print("解决方案: 重新捕获元素或确保元素包含有效的窗口句柄")
                return False
            
            # 检测应用类型
            try:
                app_type = self._detect_application_type(element.window_handle)
            except Exception as e:
                print(f"检测应用类型失败: {type(e).__name__}: {str(e)}")
                app_type = 'Unknown'
            
            # 根据应用类型选择合适的backend
            if app_type == 'Qt' or app_type in ['MFC', 'WinForms']:
                backends = ['win32', 'uia']  # 优先尝试win32 backend
            elif app_type == 'WPF':
                backends = ['uia', 'win32']  # 优先尝试uia backend
            else:
                backends = ['uia', 'win32']  # 默认先尝试uia backend
            
            print(f"测试定位: 应用类型={app_type}, 尝试backends={backends}")
            
            # 尝试不同的backend
            for backend in backends:
                try:
                    # 使用pywinauto测试定位
                    print(f"尝试使用{backend} backend定位...")
                    app = pywinauto.Application(backend=backend).connect(handle=element.window_handle)
                    window = app.window(handle=element.window_handle)
                    
                    # 检查窗口是否存在
                    if not window.exists():
                        print(f"{backend} backend: 窗口不存在")
                        continue
                    
                    # 根据元素属性构建定位条件
                    conditions_list = []
                    
                    # 条件1: 使用automation_id
                    if element.automation_id:
                        conditions = {'auto_id' if backend == 'uia' else 'id': element.automation_id}
                        conditions_list.append(("Automation ID", conditions))
                    
                    # 条件2: 使用名称
                    if element.name:
                        conditions = {'name': element.name}
                        conditions_list.append(("Name", conditions))
                    
                    # 条件3: 使用类名
                    if element.class_name:
                        conditions = {'class_name': element.class_name}
                        conditions_list.append(("Class Name", conditions))
                    
                    # 条件4: 使用名称+类名
                    if element.name and element.class_name:
                        conditions = {'name': element.name, 'class_name': element.class_name}
                        conditions_list.append(("Name+Class Name", conditions))
                    
                    # 条件5: 使用control_type
                    if element.control_type:
                        conditions = {'control_type': element.control_type}
                        conditions_list.append(("Control Type", conditions))
                    
                    if not conditions_list:
                        print(f"{backend} backend: 元素缺少定位属性")
                        continue
                    
                    # 尝试不同的定位条件
                    for condition_name, conditions in conditions_list:
                        try:
                            print(f"  尝试条件: {condition_name} = {conditions}")
                            found_element = window.child_window(**conditions)
                            if found_element.exists():
                                print(f"  ✓ 使用{backend} backend的{condition_name}定位成功")
                                return True
                            else:
                                print(f"  ✗ 使用{backend} backend的{condition_name}定位失败，元素不存在")
                        except Exception as e:
                            print(f"  ✗ 使用{backend} backend的{condition_name}定位失败: {type(e).__name__}: {str(e)}")
                    
                except Exception as e:
                    error_type = type(e).__name__
                    error_msg = str(e)
                    print(f"{backend} backend定位失败: {error_type}: {error_msg}")
                    print(f"  解决方案: 检查应用是否正在运行，窗口是否正常显示")
                    continue
            
            print("所有定位方式均失败")
            print("解决方案: ")
            print("1. 尝试重新捕获元素")
            print("2. 检查元素属性是否已变化")
            print("3. 考虑使用图像识别定位")
            print("4. 确认应用程序没有更新或重启")
            return False
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"测试元素定位失败: {error_type}: {error_msg}")
            print("解决方案: ")
            print("1. 确保元素对象有效且包含必要属性")
            print("2. 检查应用程序是否正在运行")
            print("3. 尝试重新捕获元素")
            print("4. 检查应用是否具有UIA支持")
            return False
    
    def __init__(self):
        self.capturing = False
        self.last_captured_element = None
        self.template_cache = {}  # 模板缓存
        self.screenshot_cache = None  # 截图缓存
        self.screenshot_time = 0  # 截图时间
    
    def capture_element_by_image(self, image_path, confidence=0.8):
        """通过图像识别捕获元素，使用SIFT/ORB特征匹配
        
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
                # 使用缓存的模板和特征
                template, template_gray, template_kp, template_des = self.template_cache[image_path]
            else:
                # 读取模板图像
                template = cv2.imread(image_path)
                if template is None:
                    print("无法读取模板图像")
                    return None
                
                # 图像预处理：裁剪边缘冗余区域、调整对比度
                template = self._preprocess_image(template)
                
                # 转换为灰度图
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                
                # 使用ORB特征检测器提取特征
                orb = cv2.ORB_create()
                template_kp, template_des = orb.detectAndCompute(template_gray, None)
                
                # 缓存模板和特征
                self.template_cache[image_path] = (template, template_gray, template_kp, template_des)
            
            # 获取屏幕截图，带缓存机制
            current_time = time.time()
            if self.screenshot_cache is None or current_time - self.screenshot_time > 0.5:
                # 超过0.5秒，重新截图
                screenshot = ImageGrab.grab()
                self.screenshot_cache = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                self.screenshot_time = current_time
            
            # 使用缓存的截图
            screenshot = self.screenshot_cache
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # 特征匹配
            max_val, max_loc, matched_template = self._feature_match(screenshot, screenshot_gray, template, template_kp, template_des)
            
            if max_val >= confidence:
                # 创建元素对象
                element = Element()
                element.element_type = "ImageMatched"
                element.x = max_loc[0]
                element.y = max_loc[1]
                element.width = matched_template.shape[1]
                element.height = matched_template.shape[0]
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
        if coords is None:
            return image
        x, y, w, h = cv2.boundingRect(coords)
        cropped = image[y:y+h, x:x+w]
        
        # 2. 调整对比度
        alpha = 1.2  # 对比度因子
        beta = 0     # 亮度偏移
        adjusted = cv2.convertScaleAbs(cropped, alpha=alpha, beta=beta)
        
        return adjusted
    
    def _feature_match(self, screenshot, screenshot_gray, template, template_kp, template_des):
        """使用ORB特征匹配图像
        
        Args:
            screenshot: 截图图像（彩色）
            screenshot_gray: 截图图像（灰度）
            template: 模板图像（彩色）
            template_kp: 模板特征点
            template_des: 模板特征描述符
            
        Returns:
            (匹配置信度, 匹配位置, 匹配的模板图像)
        """
        import cv2
        import numpy as np
        
        # 使用ORB特征检测器提取截图特征
        orb = cv2.ORB_create()
        screenshot_kp, screenshot_des = orb.detectAndCompute(screenshot_gray, None)
        
        # 检查是否检测到特征点
        if len(screenshot_kp) < 10 or len(template_kp) < 10:
            return 0.0, (0, 0), template
        
        # 使用BFMatcher进行特征匹配
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(template_des, screenshot_des)
        
        # 根据匹配距离排序
        matches = sorted(matches, key=lambda x: x.distance)
        
        # 计算匹配置信度
        good_matches = [m for m in matches if m.distance < 50]  # 距离阈值，可调整
        if len(good_matches) < 5:
            return 0.0, (0, 0), template
        
        confidence = min(len(good_matches) / 20.0, 1.0)  # 归一化置信度，最高1.0
        
        # 获取匹配点坐标
        template_pts = np.float32([template_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        screenshot_pts = np.float32([screenshot_kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        # 使用RANSAC计算单应性矩阵
        M, mask = cv2.findHomography(template_pts, screenshot_pts, cv2.RANSAC, 5.0)
        
        if M is None:
            return 0.0, (0, 0), template
        
        # 获取模板的边界框
        h, w = template.shape[:2]
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        
        # 转换模板边界框到截图中的位置
        dst = cv2.perspectiveTransform(pts, M)
        
        # 计算匹配位置和尺寸
        x_coords = [int(pt[0][0]) for pt in dst]
        y_coords = [int(pt[0][1]) for pt in dst]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # 确保坐标在截图范围内
        min_x = max(0, min_x)
        min_y = max(0, min_y)
        max_x = min(screenshot.shape[1], max_x)
        max_y = min(screenshot.shape[0], max_y)
        
        return confidence, (min_x, min_y), template
    
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
