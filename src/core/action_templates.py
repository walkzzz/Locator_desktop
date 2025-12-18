# -*- coding: utf-8 -*-
"""
操作示例模板模块，统一管理各种操作示例
"""

# 元素类型对应的操作模板
ACTION_TEMPLATES = {
    'Button': {
        'pywinauto': "element.click()  # 点击按钮",
        'uiautomation': "element.Click()  # 点击按钮",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击按钮",
        'win32gui': "# 发送点击消息\nlParam = win32api.MAKELONG(center_x, center_y)\nwin32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)\nwin32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)  # 点击按钮",
        'coordinate': "# 模拟鼠标点击\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 点击按钮"
    },
    'Edit': {
        'pywinauto': "element.set_text('测试文本')  # 设置文本\nelement.type_keys('{ENTER}')  # 按回车键",
        'uiautomation': "element.SendKeys('测试文本')  # 设置文本\nelement.SendKeys('{Enter}')  # 按回车键",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击输入框\npyautogui.write('测试文本')  # 输入文本\npyautogui.press('enter')  # 按回车键",
        'win32gui': "# 设置文本\nwin32gui.SetWindowText(hwnd, '测试文本')  # 设置文本",
        'coordinate': "# 点击输入框\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)\n# 输入文本\nwin32api.keybd_event(0x54, 0, 0, 0)  # T\nwin32api.keybd_event(0x65, 0, 0, 0)  # e\nwin32api.keybd_event(0x73, 0, 0, 0)  # s\nwin32api.keybd_event(0x74, 0, 0, 0)  # t\nwin32api.keybd_event(0x0D, 0, 0, 0)  # Enter"
    },
    'ComboBox': {
        'pywinauto': "element.select('选项值')  # 选择选项",
        'uiautomation': "element.Select('选项值')  # 选择选项",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击下拉框\npyautogui.press('down')  # 向下箭头\npyautogui.press('enter')  # 按回车键选择",
        'win32gui': "# 下拉框操作\nwin32gui.SendMessage(hwnd, win32con.CBM_GETCOUNT, 0, 0)  # 获取选项数量\nwin32gui.SendMessage(hwnd, win32con.CBM_SETCURSEL, 0, 0)  # 选择第一个选项",
        'coordinate': "# 点击下拉框\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)\n# 选择选项\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'CheckBox': {
        'pywinauto': "element.toggle()  # 切换选中状态",
        'uiautomation': "element.ToggleCheckState()  # 切换选中状态",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 切换复选框状态",
        'win32gui': "win32gui.SendMessage(hwnd, win32con.BM_CLICK, 0, 0)  # 切换复选框状态",
        'coordinate': "# 切换复选框状态\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'RadioButton': {
        'pywinauto': "element.click()  # 选择单选按钮",
        'uiautomation': "element.Click()  # 选择单选按钮",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 选择单选按钮",
        'win32gui': "win32gui.SendMessage(hwnd, win32con.BM_CLICK, 0, 0)  # 选择单选按钮",
        'coordinate': "# 选择单选按钮\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'List': {
        'pywinauto': "element.select('列表项')  # 选择列表项",
        'uiautomation': "element.SelectItem('列表项')  # 选择列表项",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击列表\npyautogui.press('down')  # 向下箭头\npyautogui.press('enter')  # 选择列表项",
        'win32gui': "# 列表操作\nwin32gui.SendMessage(hwnd, win32con.LB_SETCURSEL, 0, 0)  # 选择第一个列表项",
        'coordinate': "# 点击列表\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'MenuItem': {
        'pywinauto': "element.click()  # 点击菜单项",
        'uiautomation': "element.Click()  # 点击菜单项",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击菜单项",
        'win32gui': "# 菜单项操作\n# 菜单项操作通常需要先打开菜单，然后点击菜单项",
        'coordinate': "# 点击菜单项\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'Tab': {
        'pywinauto': "element.select('选项卡')  # 选择选项卡",
        'uiautomation': "element.Select('选项卡')  # 选择选项卡",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 选择选项卡",
        'win32gui': "# 选项卡操作\nwin32gui.SendMessage(hwnd, win32con.TCM_SETCURFOCUS, 0, 0)  # 选择第一个选项卡",
        'coordinate': "# 选择选项卡\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'TreeItem': {
        'pywinauto': "element.expand()  # 展开树节点",
        'uiautomation': "element.Expand()  # 展开树节点",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 展开/折叠树节点",
        'win32gui': "# 树节点操作\nwin32gui.SendMessage(hwnd, win32con.TVM_EXPAND, win32con.TVE_EXPAND, 0)  # 展开树节点",
        'coordinate': "# 点击树节点\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'Image': {
        'pywinauto': "element.click()  # 点击图像",
        'uiautomation': "element.Click()  # 点击图像",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击图像",
        'win32gui': "# 点击图像\nwin32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)\nwin32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)",
        'coordinate': "# 点击图像\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'Slider': {
        'pywinauto': "element.set_value(50)  # 设置滑块值",
        'uiautomation': "element.SetValue(50)  # 设置滑块值",
        'pyautogui': "pyautogui.click(center_x, center_y)  # 点击滑块",
        'win32gui': "# 滑块操作\nwin32gui.SendMessage(hwnd, win32con.TBM_SETPOS, 1, 50)  # 设置滑块位置为50%",
        'coordinate': "# 拖动滑块\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\n# 向右拖动50像素\nwin32api.SetCursorPos((center_x + 50, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'Default': {
        'pywinauto': "# 请根据元素类型添加相应的操作",
        'uiautomation': "# 请根据元素类型添加相应的操作",
        'pyautogui': "# 请根据元素类型添加相应的操作",
        'win32gui': "# 请根据元素类型添加相应的操作",
        'coordinate': "# 请根据元素类型添加相应的操作"
    }
}

# 其他通用操作模板
GENERAL_ACTIONS = {
    'context_menu': {
        'pywinauto': "element.right_click()  # 右键点击",
        'uiautomation': "element.RightClick()  # 右键点击",
        'pyautogui': "pyautogui.rightClick(center_x, center_y)  # 右键点击",
        'win32gui': "# 右键点击\nlParam = win32api.MAKELONG(center_x, center_y)\nwin32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)\nwin32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)",
        'coordinate': "# 右键点击\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)"
    },
    'double_click': {
        'pywinauto': "element.double_click_input()  # 双击",
        'uiautomation': "element.DoubleClick()  # 双击",
        'pyautogui': "pyautogui.doubleClick(center_x, center_y)  # 双击",
        'win32gui': "# 双击\nlParam = win32api.MAKELONG(center_x, center_y)\nwin32gui.SendMessage(hwnd, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, lParam)",
        'coordinate': "# 双击\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    },
    'drag_drop': {
        'pywinauto': "element.drag_mouse_input(dst=(x, y))  # 拖拽到指定位置",
        'uiautomation': "element.DragDrop(x, y)  # 拖拽到指定位置",
        'pyautogui': "pyautogui.dragTo(x, y, duration=0.5)  # 拖拽到指定位置",
        'win32gui': "# 拖拽操作\n# 这里需要根据实际情况实现拖拽逻辑",
        'coordinate': "# 拖拽操作\nwin32api.SetCursorPos((center_x, center_y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)\n# 拖动到目标位置\nwin32api.SetCursorPos((x, y))\nwin32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)"
    }
}
