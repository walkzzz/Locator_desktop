# -*- coding: utf-8 -*-
"""
代码生成模板模块，统一管理各种代码模板
"""

# pywinauto代码模板
PYWINAUTO_TEMPLATES = {
    'import': "from pywinauto.application import Application\n",
    'connect': "# 连接到应用\napp = Application(backend='uia').connect(process={process_id})\n",
    'window': "# 获取窗口\nwindow = app.window(handle={window_handle})\n",
    'element': "# 定位元素\nelement = window.child_window({conditions})\n",
    'action_template': "# 操作示例\n{action}\n"
}

# uiautomation代码模板
UIAUTOMATION_TEMPLATES = {
    'import': "import uiautomation as auto\n",
    'element': "# 定位元素\nelement = {element_path}\n",
    'action_template': "# 操作示例\n{action}\n"
}

# pyautogui代码模板
PYAUTOGUI_TEMPLATES = {
    'import': "import pyautogui\n",
    'coordinate': "# 元素坐标\nx = {x}\ny = {y}\nwidth = {width}\nheight = {height}\n",
    'center': "# 计算元素中心坐标\ncenter_x = x + width // 2\ncenter_y = y + height // 2\n",
    'action_template': "# 操作示例\n{action}\n"
}

# win32gui代码模板
WIN32GUI_TEMPLATES = {
    'import': "import win32gui\nimport win32api\nimport win32con\n",
    'element_info': "# 元素信息\nelement_rect = ({x}, {y}, {right}, {bottom})\n",
    'window_handle': "# 获取窗口句柄\nhwnd = win32gui.WindowFromPoint((x, y))\n",
    'window_check': "if hwnd:\n    print(f\"找到窗口: {win32gui.GetWindowText(hwnd)}\")\n    ",
    'center': "    # 计算元素中心坐标\n    center_x = x + width // 2\n    center_y = y + height // 2\n",
    'action_template': "    # 操作示例\n    {action}\n"
}

# 图像识别代码模板
IMAGE_RECOGNITION_TEMPLATES = {
    'import': "import cv2\nimport numpy as np\nfrom PIL import ImageGrab\nimport win32api\nimport win32con\n",
    'template': "# 读取模板图像（需要提前截图保存）\ntemplate_path = '{template_path}'\ntemplate = cv2.imread(template_path)\n",
    'screenshot': "# 获取屏幕截图\nscreenshot = ImageGrab.grab()\nscreenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)\n",
    'match': "# 模板匹配\nresult = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)\nmin_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)\n",
    'threshold': "# 设置匹配阈值\nthreshold = {threshold}\n",
    'condition': "if max_val >= threshold:\n",
    'center': "    # 计算元素中心坐标\n    center_x = max_loc[0] + template.shape[1] // 2\n    center_y = max_loc[1] + template.shape[0] // 2\n",
    'action_template': "    # 操作示例\n    {action}\n",
    'else': "else:\n    print('未找到匹配元素')\n"
}

# 坐标定位代码模板
COORDINATE_TEMPLATES = {
    'import': "import win32api\nimport win32con\n",
    'coordinate': "# 元素坐标\nx = {x}\ny = {y}\nwidth = {width}\nheight = {height}\n",
    'center': "# 计算元素中心坐标\ncenter_x = x + width // 2\ncenter_y = y + height // 2\n",
    'action_template': "# 操作示例\n{action}\n"
}