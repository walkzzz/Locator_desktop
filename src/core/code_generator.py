#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CodeGenerator:
    """定位代码生成器类"""

    def __init__(self):
        pass
    
    def generate_pywinauto_code(self, element):
        """生成pywinauto定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            pywinauto定位代码字符串
        """
        if not element:
            return ""
        
        # 构建应用连接代码
        app_code = f"# 连接到应用\napp = Application(backend='uia').connect(process={element.process_id})\n"
        
        # 构建窗口定位代码
        window_code = f"# 获取窗口\nwindow = app.window(handle={element.window_handle})\n"
        
        # 构建元素定位代码
        element_code = self._build_pywinauto_element_code(element)
        
        # 构建操作示例代码
        action_code = self._build_pywinauto_action_code(element)
        
        return f"from pywinauto.application import Application\n\n{app_code}{window_code}{element_code}\n{action_code}"
    
    def _build_pywinauto_element_code(self, element):
        """构建pywinauto元素定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            元素定位代码字符串
        """
        # 根据元素属性构建定位条件
        conditions = []
        
        if element.automation_id:
            conditions.append(f"auto_id='{element.automation_id}'")
        
        if element.name:
            conditions.append(f"name='{element.name}'")
        
        if element.class_name:
            conditions.append(f"class_name='{element.class_name}'")
        
        # 如果没有唯一标识，使用控件类型
        if not conditions:
            conditions.append(f"control_type='{element.element_type}'")
        
        # 构建定位表达式
        condition_str = ", ".join(conditions)
        
        return f"# 定位元素\nelement = window.child_window({condition_str})"
    
    def _build_pywinauto_action_code(self, element):
        """构建pywinauto操作示例代码
        
        Args:
            element: 元素对象
            
        Returns:
            操作示例代码字符串
        """
        action_map = {
            'Button': "element.click()  # 点击按钮",
            'Edit': "element.set_text('测试文本')  # 设置文本\nelement.type_keys('{ENTER}')  # 按回车键",
            'ComboBox': "element.select('选项值')  # 选择选项",
            'CheckBox': "element.toggle()  # 切换选中状态",
            'RadioButton': "element.click()  # 选择单选按钮",
            'List': "element.select('列表项')  # 选择列表项",
            'MenuItem': "element.click()  # 点击菜单项"
        }
        
        action = action_map.get(element.element_type, "# 请根据元素类型添加相应的操作")
        
        return f"# 操作示例\n{action}"
    
    def generate_uiautomation_code(self, element):
        """生成uiautomation定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            uiautomation定位代码字符串
        """
        if not element:
            return ""
        
        # 构建导入代码
        import_code = "import uiautomation as auto\n\n"
        
        # 构建元素定位代码
        element_code = self._build_uiautomation_element_code(element)
        
        # 构建操作示例代码
        action_code = self._build_uiautomation_action_code(element)
        
        return f"{import_code}{element_code}\n{action_code}"
    
    def _build_uiautomation_element_code(self, element):
        """构建uiautomation元素定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            元素定位代码字符串
        """
        # 获取元素路径
        path_parts = []
        current = element
        
        while current:
            # 构建路径部分
            path_part = self._build_uiautomation_path_part(current)
            path_parts.append(path_part)
            current = current.parent
        
        # 反转路径，从根到当前元素
        path_parts.reverse()
        
        # 构建完整路径
        full_path = "".join(path_parts)
        
        return f"# 定位元素\nelement = {full_path}"
    
    def _build_uiautomation_path_part(self, element):
        """构建uiautomation路径的一部分
        
        Args:
            element: 元素对象
            
        Returns:
            路径部分字符串
        """
        # 根据元素类型选择对应的方法
        control_type_map = {
            'Window': 'WindowControl',
            'Button': 'ButtonControl',
            'Edit': 'EditControl',
            'ComboBox': 'ComboBoxControl',
            'CheckBox': 'CheckBoxControl',
            'RadioButton': 'RadioButtonControl',
            'List': 'ListControl',
            'ListItem': 'ListItemControl',
            'Group': 'GroupControl',
            'Menu': 'MenuControl',
            'MenuItem': 'MenuItemControl',
            'Tab': 'TabControl',
            'TabItem': 'TabItemControl',
            'Tree': 'TreeControl',
            'TreeItem': 'TreeItemControl',
            'DataGrid': 'DataGridControl',
            'DataItem': 'DataItemControl'
        }
        
        control_method = control_type_map.get(element.element_type, 'Control')
        
        # 根据元素属性构建定位条件
        conditions = []
        
        if element.automation_id:
            conditions.append(f"AutomationId='{element.automation_id}'")
        
        if element.name:
            conditions.append(f"Name='{element.name}'")
        
        if element.class_name:
            conditions.append(f"ClassName='{element.class_name}'")
        
        # 如果是根元素，不需要条件
        if element.parent is None:
            return f"auto.GetRootControl().{control_method}()"
        
        # 构建条件字符串
        condition_str = "".join([f", {cond}" for cond in conditions])
        
        return f".{control_method}({condition_str}, Depth={element.depth})"
    
    def _build_uiautomation_action_code(self, element):
        """构建uiautomation操作示例代码
        
        Args:
            element: 元素对象
            
        Returns:
            操作示例代码字符串
        """
        action_map = {
            'Button': "element.Click()  # 点击按钮",
            'Edit': "element.SendKeys('测试文本')  # 设置文本\nelement.SendKeys('{Enter}')  # 按回车键",
            'ComboBox': "element.Select('选项值')  # 选择选项",
            'CheckBox': "element.ToggleCheckState()  # 切换选中状态",
            'RadioButton': "element.Click()  # 选择单选按钮",
            'List': "element.SelectItem('列表项')  # 选择列表项",
            'MenuItem': "element.Click()  # 点击菜单项"
        }
        
        action = action_map.get(element.element_type, "# 请根据元素类型添加相应的操作")
        
        return f"# 操作示例\n{action}"
    
    def generate_coordinate_code(self, element):
        """生成坐标定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            坐标定位代码字符串
        """
        if not element:
            return ""
        
        code = f"# 坐标定位代码\nimport win32api\nimport win32con\n\n"
        code += f"# 元素坐标\nx = {element.x}\ny = {element.y}\nwidth = {element.width}\nheight = {element.height}\n\n"
        code += f"# 计算元素中心坐标\ncenter_x = x + width // 2\ncenter_y = y + height // 2\n\n"
        code += f"# 移动鼠标到元素中心\nwin32api.SetCursorPos((center_x, center_y))\n\n"
        code += f"# 模拟鼠标点击\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\n"
        code += f"win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
        
        return code
    
    def generate_image_recognition_code(self, element):
        """生成图像识别定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            图像识别定位代码字符串
        """
        if not element:
            return ""
        
        code = f"# 图像识别定位代码\nimport cv2\nimport numpy as np\nfrom PIL import ImageGrab\nimport win32api\nimport win32con\n\n"
        code += f"# 读取模板图像（需要提前截图保存）\ntemplate_path = 'element_template.png'\ntemplate = cv2.imread(template_path)\n\n"
        code += f"# 获取屏幕截图\nscreenshot = ImageGrab.grab()\nscreenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)\n\n"
        code += f"# 模板匹配\nresult = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)\nmin_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)\n\n"
        code += f"# 设置匹配阈值\nthreshold = 0.8\n\n"
        code += f"if max_val >= threshold:\n"
        code += f"    # 计算元素中心坐标\n"
        code += f"    center_x = max_loc[0] + template.shape[1] // 2\n"
        code += f"    center_y = max_loc[1] + template.shape[0] // 2\n\n"
        code += f"    # 移动鼠标到元素中心\n"
        code += f"    win32api.SetCursorPos((center_x, center_y))\n\n"
        code += f"    # 模拟鼠标点击\n"
        code += f"    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\n"
        code += f"    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)\n"
        code += f"else:\n"
        code += f"    print('未找到匹配元素')"
        
        return code
    
    def generate_pyautogui_code(self, element):
        """生成pyautogui定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            pyautogui定位代码字符串
        """
        if not element:
            return ""
        
        code = """import pyautogui

# 元素坐标
x = {element.x}
y = {element.y}
width = {element.width}
height = {element.height}

# 计算元素中心坐标
center_x = x + width // 2
center_y = y + height // 2

# 操作示例"""
        
        # 添加元素特定操作
        action_code = self._build_pyautogui_action_code(element)
        
        return f"{code}\n{action_code}"
    
    def _build_pyautogui_action_code(self, element):
        """构建pyautogui操作示例代码
        
        Args:
            element: 元素对象
            
        Returns:
            操作示例代码字符串
        """
        action_map = {
            'Button': "# 点击按钮\npyautogui.click(center_x, center_y)\n",
            'Edit': "# 输入文本\npyautogui.click(center_x, center_y)\npyautogui.write('测试文本')\n",
            'ComboBox': "# 下拉框操作\npyautogui.click(center_x, center_y)\npyautogui.press('down')\npyautogui.press('enter')\n",
            'CheckBox': "# 切换复选框\npyautogui.click(center_x, center_y)\n",
            'RadioButton': "# 选择单选按钮\npyautogui.click(center_x, center_y)\n",
            'MenuItem': "# 点击菜单项\npyautogui.click(center_x, center_y)\n"
        }
        
        return action_map.get(element.element_type, f"# 根据元素类型添加操作\npyautogui.click(center_x, center_y)\n")
    
    def generate_win32gui_code(self, element):
        """生成win32gui定位代码
        
        Args:
            element: 元素对象
            
        Returns:
            win32gui定位代码字符串
        """
        if not element:
            return ""
        
        code = """import win32gui
import win32api
import win32con

# 元素信息
element_rect = ({element.x}, {element.y}, {element.x + element.width}, {element.y + element.height})

# 获取窗口句柄
hwnd = win32gui.WindowFromPoint((element.x, element.y))

if hwnd:
    print(f"找到窗口: {win32gui.GetWindowText(hwnd)}")
    
    # 计算元素中心坐标
    center_x = element.x + element.width // 2
    center_y = element.y + element.height // 2
    
    # 操作示例"""
        
        # 添加元素特定操作
        action_code = self._build_win32gui_action_code(element)
        
        return f"{code}\n{action_code}\n"
    
    def _build_win32gui_action_code(self, element):
        """构建win32gui操作示例代码
        
        Args:
            element: 元素对象
            
        Returns:
            操作示例代码字符串
        """
        action_map = {
            'Button': "    # 发送点击消息\n    lParam = win32api.MAKELONG(center_x, center_y)\n    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)\n    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)\n",
            'Edit': "    # 设置文本\n    win32gui.SetWindowText(hwnd, '测试文本')\n",
            'ComboBox': "    # 下拉框操作\n    # 这里需要根据实际情况调整消息类型\n    win32gui.SendMessage(hwnd, win32con.CBM_GETCOUNT, 0, 0)\n    win32gui.SendMessage(hwnd, win32con.CBM_SETCURSEL, 0, 0)\n",
            'CheckBox': "    # 切换复选框状态\n    win32gui.SendMessage(hwnd, win32con.BM_CLICK, 0, 0)\n",
            'RadioButton': "    # 选择单选按钮\n    win32gui.SendMessage(hwnd, win32con.BM_CLICK, 0, 0)\n"
        }
        
        return action_map.get(element.element_type, "    # 根据元素类型添加win32gui操作\n")
    
    def generate_code_by_method(self, element, method):
        """根据指定方法生成定位代码
        
        Args:
            element: 元素对象
            method: 定位方法，可选值：auto, attribute, image, coordinate, pyautogui, win32gui
            
        Returns:
            定位代码字符串
        """
        if method == 'auto':
            # 自动选择最佳定位方式
            if element.automation_id or element.name or element.class_name:
                return self.generate_pywinauto_code(element)
            else:
                return self.generate_image_recognition_code(element)
        elif method == 'attribute':
            return self.generate_pywinauto_code(element)
        elif method == 'image':
            return self.generate_image_recognition_code(element)
        elif method == 'coordinate':
            return self.generate_coordinate_code(element)
        elif method == 'pyautogui':
            return self.generate_pyautogui_code(element)
        elif method == 'win32gui':
            return self.generate_win32gui_code(element)
        else:
            return "# 不支持的定位方法"
