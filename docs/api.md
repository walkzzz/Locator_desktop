# Locator_desktop API文档

## 1. 概述

本文档详细描述了Locator_desktop工具的API接口，包括各个模块、类和方法的使用方式。API文档分为以下几个部分：

- Element模块：元素数据结构
- ElementCapture模块：元素捕获核心逻辑
- ElementAnalyzer模块：元素分析和树构建
- CodeGenerator模块：定位代码生成器
- WindowUtils模块：窗口管理工具
- ProcessUtils模块：进程管理工具

## 2. Element模块

### 2.1 模块概述

Element模块定义了元素的数据结构，用于存储和管理UI元素的各种属性和状态。

### 2.2 Element类

**类签名**：`class Element`

**功能**：表示UI元素的基本数据结构，包含元素的属性、状态和层次关系。

#### 属性

| 属性名 | 类型 | 描述 | 默认值 |
|--------|------|------|--------|
| `element_id` | `Any` | 元素唯一标识 | `None` |
| `name` | `str` | 元素名称 | `None` |
| `element_type` | `str` | 元素类型 | `None` |
| `control_type` | `str` | 控件类型 | `None` |
| `class_name` | `str` | 类名 | `None` |
| `automation_id` | `str` | Automation ID | `None` |
| `x` | `int` | 元素左上角x坐标 | `None` |
| `y` | `int` | 元素左上角y坐标 | `None` |
| `width` | `int` | 元素宽度 | `None` |
| `height` | `int` | 元素高度 | `None` |
| `parent` | `Element` | 父元素 | `None` |
| `children` | `List[Element]` | 子元素列表 | `[]` |
| `depth` | `int` | 元素深度 | `0` |
| `is_enabled` | `bool` | 是否可用 | `None` |
| `is_visible` | `bool` | 是否可见 | `None` |
| `is_checked` | `bool` | 是否被选中 | `None` |
| `text` | `str` | 元素文本内容 | `None` |
| `process_id` | `int` | 所属进程ID | `None` |
| `window_handle` | `int` | 所属窗口句柄 | `None` |
| `attributes` | `Dict[str, Any]` | 其他自定义属性 | `{}` |

#### 方法

##### `__init__()`

**功能**：初始化Element实例。

**参数**：无

**返回值**：`None`

##### `__str__()`

**功能**：返回元素的字符串表示。

**参数**：无

**返回值**：`str` - 元素的字符串表示，格式为：`{element_type} - {name} ({x}, {y}) [{width}x{height}]`

##### `add_child(child: Element)`

**功能**：添加子元素。

**参数**：
- `child`：`Element` - 要添加的子元素

**返回值**：`None`

**示例**：
```python
parent_element = Element()
child_element = Element()
parent_element.add_child(child_element)
```

##### `get_path()`

**功能**：获取元素的完整路径。

**参数**：无

**返回值**：`str` - 元素路径，格式为：`RootElementType(RootName) > ParentElementType(ParentName) > CurrentElementType(CurrentName)`

**示例**：
```python
element = Element()
path = element.get_path()
print(path)  # 输出："Window(MainWindow) > Button(OK)"
```

## 3. ElementCapture模块

### 3.1 模块概述

ElementCapture模块负责元素捕获，支持多种捕获方式，包括鼠标悬停捕获和图像识别捕获。

### 3.2 ElementCapture类

**类签名**：`class ElementCapture`

**功能**：实现元素捕获的核心逻辑，支持多种捕获方式。

#### 属性

| 属性名 | 类型 | 描述 | 默认值 |
|--------|------|------|--------|
| `capturing` | `bool` | 是否正在捕获元素 | `False` |
| `last_captured_element` | `Element` | 上次捕获的元素 | `None` |

#### 方法

##### `__init__()`

**功能**：初始化ElementCapture实例。

**参数**：无

**返回值**：`None`

##### `capture_element()`

**功能**：捕获元素，支持鼠标悬停捕获。

**参数**：无

**返回值**：`Element` - 捕获到的元素对象，如果没有捕获到返回`None`

**示例**：
```python
capture = ElementCapture()
element = capture.capture_element()
if element:
    print(f"捕获到元素: {element}")
```

##### `test_element_location(element: Element)`

**功能**：测试元素定位是否有效。

**参数**：
- `element`：`Element` - 要测试的元素对象

**返回值**：`bool` - 定位是否成功

**示例**：
```python
capture = ElementCapture()
element = capture.capture_element()
if element:
    success = capture.test_element_location(element)
    print(f"定位测试结果: {'成功' if success else '失败'}")
```

##### `capture_element_by_image(image_path: str, confidence: float = 0.8)`

**功能**：通过图像识别捕获元素。

**参数**：
- `image_path`：`str` - 模板图像文件路径
- `confidence`：`float` - 识别置信度，默认值为0.8

**返回值**：`Element` - 识别到的元素对象，如果没有识别到返回`None`

**示例**：
```python
capture = ElementCapture()
element = capture.capture_element_by_image("button_template.png", confidence=0.9)
if element:
    print(f"图像识别捕获到元素: {element}")
```

## 4. ElementAnalyzer模块

### 4.1 模块概述

ElementAnalyzer模块负责元素分析和树构建，将窗口的UI元素转换为结构化的元素树。

### 4.2 ElementAnalyzer类

**类签名**：`class ElementAnalyzer`

**功能**：实现元素分析和树构建的核心逻辑。

#### 属性

| 属性名 | 类型 | 描述 | 默认值 |
|--------|------|------|--------|
| `max_depth` | `int` | 最大分析深度 | `10` |

#### 方法

##### `__init__(max_depth: int = 10)`

**功能**：初始化ElementAnalyzer实例。

**参数**：
- `max_depth`：`int` - 最大分析深度，默认值为10

**返回值**：`None`

##### `analyze_window(window)`

**功能**：分析窗口的UI元素结构，构建元素树。

**参数**：
- `window`：`Any` - 窗口对象，必须包含`hwnd`属性

**返回值**：`Element` - 窗口的根元素对象，如果分析失败返回`None`

**示例**：
```python
analyzer = ElementAnalyzer()
window = WindowUtils.get_window_by_title("测试窗口")
if window:
    root_element = analyzer.analyze_window(window)
    if root_element:
        print(f"成功构建元素树，根元素: {root_element}")
```

##### `get_element_path(element: Element)`

**功能**：获取元素的定位路径。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 元素定位路径，格式为XML-like字符串

**示例**：
```python
analyzer = ElementAnalyzer()
element = Element()
path = analyzer.get_element_path(element)
print(path)
# 输出：
# <Window automation_id="main_window" depth=1>
# <Button name="OK" depth=2>
```

##### `analyze_element_compatibility(element: Element)`

**功能**：分析元素的兼容性，提供优化建议。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`Dict` - 兼容性分析结果，包含以下字段：
  - `pywinauto_support`：`bool` - 是否支持pywinauto
  - `uiautomation_support`：`bool` - 是否支持uiautomation
  - `recommended_method`：`str` - 推荐的定位方式（auto/attribute/image/coordinate）
  - `issues`：`List[str]` - 兼容性问题列表

**示例**：
```python
analyzer = ElementAnalyzer()
element = Element()
compatibility = analyzer.analyze_element_compatibility(element)
print(f"推荐定位方式: {compatibility['recommended_method']}")
if compatibility['issues']:
    print(f"兼容性问题: {', '.join(compatibility['issues'])}")
```

##### `get_element_unique_identifier(element: Element)`

**功能**：获取元素的唯一标识符。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 元素的唯一标识符，优先使用automation_id，其次是name+type，最后是class_name+type

**示例**：
```python
analyzer = ElementAnalyzer()
element = Element()
element.automation_id = "button_ok"
identifier = analyzer.get_element_unique_identifier(element)
print(identifier)  # 输出："automation_id='button_ok'"
```

## 5. CodeGenerator模块

### 5.1 模块概述

CodeGenerator模块负责根据元素信息生成定位代码，支持多种定位方式和自动化库。

### 5.2 CodeGenerator类

**类签名**：`class CodeGenerator`

**功能**：实现定位代码生成的核心逻辑，支持多种定位方式和自动化库。

#### 方法

##### `__init__()`

**功能**：初始化CodeGenerator实例。

**参数**：无

**返回值**：`None`

##### `generate_pywinauto_code(element: Element)`

**功能**：生成pywinauto定位代码。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 生成的pywinauto定位代码

**示例**：
```python
generator = CodeGenerator()
element = Element()
element.process_id = 1234
element.window_handle = 5678
element.automation_id = "button_ok"
code = generator.generate_pywinauto_code(element)
print(code)
# 输出：
# from pywinauto.application import Application
#
# # 连接到应用
# app = Application(backend='uia').connect(process=1234)
# # 获取窗口
# window = app.window(handle=5678)
# # 定位元素
# element = window.child_window(auto_id='button_ok')
# # 操作示例
# element.click()  # 点击按钮
```

##### `generate_uiautomation_code(element: Element)`

**功能**：生成uiautomation定位代码。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 生成的uiautomation定位代码

**示例**：
```python
generator = CodeGenerator()
element = Element()
element.automation_id = "button_ok"
element.depth = 2
code = generator.generate_uiautomation_code(element)
print(code)
# 输出：
# import uiautomation as auto
#
# # 定位元素
# element = auto.GetRootControl().WindowControl().ButtonControl(AutomationId='button_ok', Depth=2)
# # 操作示例
# element.Click()  # 点击按钮
```

##### `generate_coordinate_code(element: Element)`

**功能**：生成坐标定位代码。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 生成的坐标定位代码

**示例**：
```python
generator = CodeGenerator()
element = Element()
element.x = 100
element.y = 200
element.width = 50
element.height = 30
code = generator.generate_coordinate_code(element)
print(code)
# 输出：
# # 坐标定位代码
# import win32api
# import win32con
#
# # 元素坐标
# x = 100
# y = 200
# width = 50
# height = 30
#
# # 计算元素中心坐标
# center_x = x + width // 2
# center_y = y + height // 2
#
# # 移动鼠标到元素中心
# win32api.SetCursorPos((center_x, center_y))
#
# # 模拟鼠标点击
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
```

##### `generate_image_recognition_code(element: Element)`

**功能**：生成图像识别定位代码。

**参数**：
- `element`：`Element` - 元素对象

**返回值**：`str` - 生成的图像识别定位代码

**示例**：
```python
generator = CodeGenerator()
element = Element()
code = generator.generate_image_recognition_code(element)
print(code)
# 输出：
# # 图像识别定位代码
# import cv2
# import numpy as np
# from PIL import ImageGrab
# import win32api
# import win32con
#
# # 读取模板图像（需要提前截图保存）
# template_path = 'element_template.png'
# template = cv2.imread(template_path)
#
# # 获取屏幕截图
# screenshot = ImageGrab.grab()
# screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#
# # 模板匹配
# result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#
# # 设置匹配阈值
# threshold = 0.8
#
# if max_val >= threshold:
#     # 计算元素中心坐标
#     center_x = max_loc[0] + template.shape[1] // 2
#     center_y = max_loc[1] + template.shape[0] // 2
#
#     # 移动鼠标到元素中心
#     win32api.SetCursorPos((center_x, center_y))
#
#     # 模拟鼠标点击
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
# else:
#     print('未找到匹配元素')
```

##### `generate_code_by_method(element: Element, method: str)`

**功能**：根据指定方法生成定位代码。

**参数**：
- `element`：`Element` - 元素对象
- `method`：`str` - 定位方法，可选值：
  - `auto`：自动选择最佳定位方式
  - `attribute`：属性定位
  - `image`：图像识别定位
  - `coordinate`：坐标定位

**返回值**：`str` - 生成的定位代码

**示例**：
```python
generator = CodeGenerator()
element = Element()
# 自动选择定位方式
code = generator.generate_code_by_method(element, method="auto")
# 强制使用属性定位
attribute_code = generator.generate_code_by_method(element, method="attribute")
```

## 6. WindowUtils模块

### 6.1 模块概述

WindowUtils模块提供窗口管理相关的工具函数，用于获取和操作窗口。

### 6.2 方法

##### `get_all_windows()`

**功能**：获取所有可见窗口。

**参数**：无

**返回值**：`List[Window]` - 可见窗口列表

**示例**：
```python
windows = WindowUtils.get_all_windows()
for window in windows:
    print(f"窗口标题: {window.title}, 句柄: {window.hwnd}")
```

##### `get_window_by_title(title: str, exact_match: bool = False)`

**功能**：根据标题获取窗口。

**参数**：
- `title`：`str` - 窗口标题
- `exact_match`：`bool` - 是否精确匹配，默认值为`False`

**返回值**：`Window` - 匹配的窗口对象，如果没有找到返回`None`

**示例**：
```python
# 模糊匹配
window = WindowUtils.get_window_by_title("记事本")
# 精确匹配
window = WindowUtils.get_window_by_title("无标题 - 记事本", exact_match=True)
```

##### `get_windows_by_pid(pid: int)`

**功能**：根据进程ID获取窗口。

**参数**：
- `pid`：`int` - 进程ID

**返回值**：`List[Window]` - 匹配的窗口列表

**示例**：
```python
windows = WindowUtils.get_windows_by_pid(1234)
for window in windows:
    print(f"窗口标题: {window.title}")
```

##### `get_window_rect(window)`

**功能**：获取窗口矩形区域。

**参数**：
- `window`：`Any` - 窗口对象或句柄

**返回值**：`Tuple[int, int, int, int]` - 窗口矩形，格式为：`(left, top, right, bottom)`

**示例**：
```python
window = WindowUtils.get_window_by_title("记事本")
rect = WindowUtils.get_window_rect(window)
print(f"窗口矩形: {rect}")  # 输出："窗口矩形: (100, 100, 500, 400)"
```

##### `activate_window(window)`

**功能**：激活窗口。

**参数**：
- `window`：`Any` - 窗口对象或句柄

**返回值**：`None`

**示例**：
```python
window = WindowUtils.get_window_by_title("记事本")
WindowUtils.activate_window(window)
```

## 7. ProcessUtils模块

### 7.1 模块概述

ProcessUtils模块提供进程管理相关的工具函数，用于获取和操作进程。

### 7.2 方法

##### `get_running_processes()`

**功能**：获取所有正在运行的进程。

**参数**：无

**返回值**：`List[Process]` - 正在运行的进程列表

**示例**：
```python
processes = ProcessUtils.get_running_processes()
for process in processes:
    print(f"进程名: {process.name}, PID: {process.pid}")
```

##### `get_process_by_pid(pid: int)`

**功能**：根据进程ID获取进程信息。

**参数**：
- `pid`：`int` - 进程ID

**返回值**：`Process` - 进程对象，如果没有找到返回`None`

**示例**：
```python
process = ProcessUtils.get_process_by_pid(1234)
if process:
    print(f"进程名: {process.name}, 可执行路径: {process.exe}")
```

##### `get_process_by_name(name: str)`

**功能**：根据进程名获取进程列表。

**参数**：
- `name`：`str` - 进程名

**返回值**：`List[Process]` - 匹配的进程列表

**示例**：
```python
processes = ProcessUtils.get_process_by_name("notepad.exe")
for process in processes:
    print(f"PID: {process.pid}")
```

##### `is_process_running(pid: int)`

**功能**：检查进程是否正在运行。

**参数**：
- `pid`：`int` - 进程ID

**返回值**：`bool` - 进程是否正在运行

**示例**：
```python
is_running = ProcessUtils.is_process_running(1234)
print(f"进程是否运行: {'是' if is_running else '否'}")
```

## 8. 异常处理

### 8.1 常见异常

| 异常类型 | 描述 | 可能的原因 |
|----------|------|------------|
| `ElementNotFoundError` | 元素未找到 | 元素已关闭或不可见 |
| `WindowNotFoundError` | 窗口未找到 | 窗口已关闭或标题变更 |
| `ProcessNotFoundError` | 进程未找到 | 进程已结束 |
| `CaptureTimeoutError` | 捕获超时 | 元素捕获超时 |
| `ImageRecognitionError` | 图像识别失败 | 模板图像不匹配或质量差 |

### 8.2 异常处理示例

```python
from core.exceptions import ElementNotFoundError, WindowNotFoundError

try:
    # 尝试获取窗口
    window = WindowUtils.get_window_by_title("不存在的窗口")
    if not window:
        raise WindowNotFoundError("窗口未找到")
    
    # 尝试捕获元素
    capture = ElementCapture()
    element = capture.capture_element()
    if not element:
        raise ElementNotFoundError("元素未找到")
    
except WindowNotFoundError as e:
    print(f"窗口错误: {e}")
except ElementNotFoundError as e:
    print(f"元素错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 9. 使用示例

### 9.1 完整定位流程

```python
from core.element_capture import ElementCapture
from core.element_analyzer import ElementAnalyzer
from core.code_generator import CodeGenerator
from utils.window_utils import WindowUtils

# 1. 选择目标窗口
window = WindowUtils.get_window_by_title("记事本")
if not window:
    print("未找到目标窗口")
    exit()

# 2. 分析窗口元素
alyzer = ElementAnalyzer()
root_element = analyzer.analyze_window(window)
if not root_element:
    print("元素分析失败")
    exit()

# 3. 捕获目标元素
capture = ElementCapture()
element = capture.capture_element()
if not element:
    print("元素捕获失败")
    exit()

# 4. 生成定位代码
generator = CodeGenerator()
pywinauto_code = generator.generate_pywinauto_code(element)
uiauto_code = generator.generate_uiautomation_code(element)

# 5. 打印生成的代码
print("=== pywinauto定位代码 ===")
print(pywinauto_code)
print("\n=== uiautomation定位代码 ===")
print(uiauto_code)

# 6. 测试定位
success = capture.test_element_location(element)
print(f"\n定位测试结果: {'成功' if success else '失败'}")
```

## 10. 版本历史

| 版本 | 变更内容 | 变更时间 |
|------|----------|----------|
| 1.0.0 | 初始版本发布 | 2025-12-18 |
| 1.1.0 | 添加图像识别定位功能 | 2025-12-25 |
| 1.2.0 | 优化元素树加载性能 | 2026-01-10 |

## 11. 贡献指南

如果您想为Locator_desktop项目贡献代码，请遵循以下指南：

1. Fork项目仓库
2. 创建功能分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

## 12. 联系我们

如有任何问题或建议，请通过以下方式联系我们：

- 项目地址：[GitHub Repository]()
- 邮箱：[your-email@example.com]

---

本API文档详细描述了Locator_desktop工具的所有API接口，希望能帮助您更好地使用和扩展该工具。