# Locator_desktop 设计文档

## 1. 架构设计

### 1.1 总体架构

Locator_desktop采用分层架构设计，将应用分为UI层、核心业务逻辑层和工具层，各层之间通过明确的接口进行交互，实现高内聚、低耦合的设计目标。

```
┌───────────────────────────────────────────────────────────────────┐
│                          UI层 (UI Layer)                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                     MainWindow                          │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────┐
│                     核心业务逻辑层 (Core Layer)                   │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │  ElementCapture │  │ ElementAnalyzer │  │ CodeGenerator   │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│                                                                   │
│  ┌─────────────────┐                                             │
│  │     Element     │                                             │
│  └─────────────────┘                                             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────┐
│                           工具层 (Utils Layer)                    │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐                        │
│  │  WindowUtils    │  │  ProcessUtils   │                        │
│  └─────────────────┘  └─────────────────┘                        │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────┐
│                        外部依赖层 (External Layer)                │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │    pywinauto    │  │ uiautomation    │  │  opencv-python  │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │    pygetwindow  │  │     psutil      │  │     PyQt5       │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 1.2 核心模块关系

各核心模块之间的关系如下：

- **MainWindow**：作为应用的入口，负责UI展示和用户交互，调用其他模块完成业务逻辑
- **ElementCapture**：负责元素捕获，与外部依赖库交互，获取元素信息
- **ElementAnalyzer**：负责元素分析和树构建，处理捕获到的元素信息
- **CodeGenerator**：根据元素信息生成定位代码
- **WindowUtils**：提供窗口管理相关的工具函数
- **ProcessUtils**：提供进程管理相关的工具函数

## 2. 模块设计

### 2.1 UI层设计

#### 2.1.1 主窗口设计

主窗口采用分割布局，将界面分为四个主要区域：

1. **应用程序选择区域**：位于顶部，包含应用路径输入框、查找按钮和捕获按钮
2. **左侧面板**：包含进程列表、窗口列表和元素树
3. **右侧上方面板**：包含元素详细信息和定位路径
4. **右侧下方面板**：包含定位方式选择和定位代码生成

#### 2.1.2 界面流程图

```
┌───────────────────────────────────────────────────────────────────┐
│                        应用程序选择区域                          │
│  ┌─────────────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │  应用路径输入框  │  │ 查找下一个│  │ 查找上一个│  │ 捕获元素按钮│  │
│  └─────────────────┘  └─────────┘  └─────────┘  └─────────────┘  │
└───────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────────┐
│                        主分割器 (水平)                            │
│                                                                   │
│  ┌─────────────────────────┐  ┌─────────────────────────────────┐  │
│  │       左侧面板         │  │       右侧分割器 (垂直)          │  │
│  │                         │  │                                 │  │
│  │  ┌─────────────────┐   │  │  ┌─────────────────────────┐   │  │
│  │  │   进程选择      │   │  │  │     元素详细信息       │   │  │
│  │  └─────────────────┘   │  │  └─────────────────────────┘   │  │
│  │                         │  │                                 │  │
│  │  ┌─────────────────┐   │  │  ┌─────────────────────────┐   │  │
│  │  │   窗口选择      │   │  │  │     定位方式选择       │   │  │
│  │  └─────────────────┘   │  │  └─────────────────────────┘   │  │
│  │                         │  │                                 │  │
│  │  ┌─────────────────┐   │  │  ┌─────────────────────────┐   │  │
│  │  │   元素树        │   │  │  │     定位代码生成       │   │  │
│  │  └─────────────────┘   │  │  └─────────────────────────┘   │  │
│  └─────────────────────────┘  └─────────────────────────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 核心业务逻辑层设计

#### 2.2.1 Element模块

**功能**：定义元素的数据结构，存储元素的各种属性和状态

**核心属性**：
- `element_id`：元素唯一标识
- `name`：元素名称
- `element_type`：元素类型
- `control_type`：控件类型
- `class_name`：类名
- `automation_id`：Automation ID
- `x, y, width, height`：元素位置和尺寸
- `parent`：父元素
- `children`：子元素列表
- `depth`：元素深度
- `is_enabled, is_visible, is_checked`：元素状态
- `attributes`：其他自定义属性

#### 2.2.2 ElementCapture模块

**功能**：负责元素捕获，支持多种捕获方式

**核心方法**：
- `capture_element()`：捕获元素，支持鼠标悬停捕获
- `_get_element_by_coordinate()`：根据坐标获取元素
- `_convert_to_element()`：将外部库元素转换为自定义Element对象
- `test_element_location()`：测试元素定位是否有效
- `capture_element_by_image()`：通过图像识别捕获元素

#### 2.2.3 ElementAnalyzer模块

**功能**：负责元素分析和树构建

**核心方法**：
- `analyze_window()`：分析窗口的UI元素结构
- `_analyze_element_children()`：递归分析元素的子元素
- `get_element_path()`：获取元素的定位路径
- `analyze_element_compatibility()`：分析元素的兼容性
- `get_element_unique_identifier()`：获取元素的唯一标识符

#### 2.2.4 CodeGenerator模块

**功能**：根据元素信息生成定位代码

**核心方法**：
- `generate_pywinauto_code()`：生成pywinauto定位代码
- `generate_uiautomation_code()`：生成uiautomation定位代码
- `generate_coordinate_code()`：生成坐标定位代码
- `generate_image_recognition_code()`：生成图像识别定位代码
- `generate_code_by_method()`：根据指定方法生成定位代码

### 2.3 工具层设计

#### 2.3.1 WindowUtils模块

**功能**：提供窗口管理相关的工具函数

**核心方法**：
- `get_all_windows()`：获取所有可见窗口
- `get_window_by_title()`：根据标题获取窗口
- `get_windows_by_pid()`：根据进程ID获取窗口
- `get_window_rect()`：获取窗口矩形区域
- `activate_window()`：激活窗口

#### 2.3.2 ProcessUtils模块

**功能**：提供进程管理相关的工具函数

**核心方法**：
- `get_running_processes()`：获取所有正在运行的进程
- `get_process_by_pid()`：根据进程ID获取进程信息
- `get_process_by_name()`：根据进程名获取进程列表
- `is_process_running()`：检查进程是否正在运行

## 3. 类设计

### 3.1 类关系图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    MainWindow   │────▶│ ElementCapture  │────▶│   Element       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       ▲                       ▲
        ▼                       │                       │
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ ElementAnalyzer │────▶│   Element       │────▶│ CodeGenerator   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       ▲
        ▼                       │
┌─────────────────┐     ┌─────────────────┐
│  WindowUtils    │     │  ProcessUtils   │
└─────────────────┘     └─────────────────┘
```

### 3.2 核心类详细设计

#### 3.2.1 Element类

| 属性名 | 类型 | 描述 | 默认值 |
|--------|------|------|--------|
| element_id | Any | 元素唯一标识 | None |
| name | str | 元素名称 | None |
| element_type | str | 元素类型 | None |
| control_type | str | 控件类型 | None |
| class_name | str | 类名 | None |
| automation_id | str | Automation ID | None |
| x | int | 元素左上角x坐标 | None |
| y | int | 元素左上角y坐标 | None |
| width | int | 元素宽度 | None |
| height | int | 元素高度 | None |
| parent | Element | 父元素 | None |
| children | List[Element] | 子元素列表 | [] |
| depth | int | 元素深度 | 0 |
| is_enabled | bool | 是否可用 | None |
| is_visible | bool | 是否可见 | None |
| is_checked | bool | 是否被选中 | None |
| text | str | 元素文本内容 | None |
| process_id | int | 所属进程ID | None |
| window_handle | int | 所属窗口句柄 | None |
| attributes | Dict[str, Any] | 其他自定义属性 | {} |

| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| __init__() | None | None | 初始化元素对象 |
| __str__() | None | str | 返回元素的字符串表示 |
| add_child() | child: Element | None | 添加子元素 |
| get_path() | None | str | 获取元素路径 |

#### 3.2.2 ElementCapture类

| 属性名 | 类型 | 描述 | 默认值 |
|--------|------|------|--------|
| capturing | bool | 是否正在捕获元素 | False |
| last_captured_element | Element | 上次捕获的元素 | None |

| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| __init__() | None | None | 初始化捕获器 |
| capture_element() | None | Element | 捕获元素 |
| _get_element_by_coordinate() | hwnd: int, x: int, y: int | Element | 根据坐标获取元素 |
| _convert_to_element() | automation_element | Element | 转换uiautomation元素 |
| _convert_pywinauto_to_element() | pywinauto_element | Element | 转换pywinauto元素 |
| test_element_location() | element: Element | bool | 测试元素定位 |
| capture_element_by_image() | image_path: str, confidence: float | Element | 图像识别捕获 |

#### 3.2.3 MainWindow类

| 属性名 | 类型 | 描述 |
|--------|------|------|
| element_capture | ElementCapture | 元素捕获实例 |
| element_analyzer | ElementAnalyzer | 元素分析实例 |
| code_generator | CodeGenerator | 代码生成器实例 |
| window_utils | WindowUtils | 窗口工具实例 |
| process_utils | ProcessUtils | 进程工具实例 |
| current_element | Element | 当前选中的元素 |

| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| __init__() | None | None | 初始化主窗口 |
| init_ui() | None | None | 初始化UI布局 |
| create_toolbar() | None | QGroupBox | 创建工具栏 |
| create_left_panel() | None | QWidget | 创建左侧面板 |
| create_right_top_panel() | None | QWidget | 创建右侧上方面板 |
| create_right_bottom_panel() | None | QWidget | 创建右侧下方面板 |
| connect_signals() | None | None | 连接信号与槽 |
| refresh_process_list() | None | None | 刷新进程列表 |
| on_process_changed() | None | None | 进程选择变化处理 |
| on_window_changed() | None | None | 窗口选择变化处理 |
| update_element_tree() | None | None | 更新元素树 |
| build_element_tree() | element: Element, parent_item: QTreeWidgetItem | None | 构建元素树 |
| on_element_selected() | item: QTreeWidgetItem, column: int | None | 元素选择处理 |
| update_element_info() | element: Element | None | 更新元素信息 |
| update_element_path() | element: Element | None | 更新元素路径 |
| generate_locator_code() | element: Element | None | 生成定位代码 |
| start_capture() | None | None | 开始捕获元素 |
| test_location() | None | None | 测试定位 |
| copy_code() | None | None | 复制代码 |

## 4. 数据设计

### 4.1 元素数据结构

元素数据结构采用面向对象设计，使用Element类表示，包含元素的所有属性和状态信息。Element类的实例在各个模块之间传递，确保数据的一致性和完整性。

### 4.2 配置数据

应用配置数据采用JSON格式存储，包含以下内容：

```json
{
  "ui": {
    "window": {
      "width": 1200,
      "height": 800,
      "x": 100,
      "y": 100
    }
  },
  "locator": {
    "default_method": "attribute",
    "image_recognition": {
      "confidence": 0.8
    }
  },
  "code_generation": {
    "default_library": "pywinauto"
  },
  "logging": {
    "level": "INFO",
    "file": "locator.log"
  }
}
```

## 5. 接口设计

### 5.1 模块间接口

| 调用方 | 被调用方 | 接口方法 | 参数 | 返回值 | 描述 |
|--------|----------|----------|------|--------|------|
| MainWindow | ElementCapture | capture_element() | None | Element | 捕获元素 |
| MainWindow | ElementAnalyzer | analyze_window() | window | Element | 分析窗口元素 |
| MainWindow | ElementAnalyzer | get_element_path() | element | str | 获取元素路径 |
| MainWindow | CodeGenerator | generate_pywinauto_code() | element | str | 生成pywinauto代码 |
| MainWindow | CodeGenerator | generate_uiautomation_code() | element | str | 生成uiautomation代码 |
| ElementCapture | WindowUtils | get_window_by_title() | title | Window | 根据标题获取窗口 |
| ElementAnalyzer | ProcessUtils | get_process_by_pid() | pid | Process | 根据PID获取进程 |

### 5.2 外部接口

| 接口名称 | 功能描述 | 调用方式 | 参数 | 返回值 |
|----------|----------|----------|------|--------|
| pywinauto.Application | 连接到应用 | app = Application(backend='uia').connect() | backend, process/path | Application实例 |
| pywinauto.WindowSpecification | 定位元素 | window.child_window() | 定位条件 | WindowSpecification实例 |
| uiautomation.AutomationElement | 从句柄获取元素 | AutomationElement.FromHandle() | hwnd | AutomationElement实例 |
| uiautomation.AutomationElement | 从点获取元素 | AutomationElement.FromPoint() | (x, y) | AutomationElement实例 |
| cv2.matchTemplate | 模板匹配 | cv2.matchTemplate() | image, template, method | result矩阵 |

## 6. 测试设计

### 6.1 测试策略

采用分层测试策略，包括单元测试、集成测试和系统测试：

1. **单元测试**：测试各个模块的独立功能，确保每个模块的功能正确性
2. **集成测试**：测试模块之间的交互，确保模块集成正常
3. **系统测试**：测试整个应用的功能，确保系统满足需求

### 6.2 测试用例设计

#### 6.2.1 单元测试用例

| 测试模块 | 测试用例 | 预期结果 |
|----------|----------|----------|
| Element | 创建Element实例 | 实例创建成功，默认属性正确 |
| Element | 添加子元素 | 子元素添加成功，父子关系正确 |
| ElementCapture | 捕获元素 | 成功捕获到元素，属性正确 |
| ElementAnalyzer | 分析窗口元素 | 成功构建元素树，层次关系正确 |
| CodeGenerator | 生成pywinauto代码 | 生成的代码格式正确，可执行 |
| CodeGenerator | 生成uiautomation代码 | 生成的代码格式正确，可执行 |
| WindowUtils | 获取窗口列表 | 成功获取所有可见窗口 |
| ProcessUtils | 获取进程列表 | 成功获取所有运行中的进程 |

#### 6.2.2 集成测试用例

| 测试场景 | 测试步骤 | 预期结果 |
|----------|----------|----------|
| 元素捕获与分析 | 1. 捕获元素<br>2. 分析元素属性 | 捕获的元素属性正确，分析结果准确 |
| 元素分析与代码生成 | 1. 分析元素<br>2. 生成定位代码 | 生成的定位代码与元素属性匹配 |
| 代码生成与验证 | 1. 生成定位代码<br>2. 测试定位 | 定位测试通过，生成的代码有效 |

#### 6.2.3 系统测试用例

| 测试场景 | 测试步骤 | 预期结果 |
|----------|----------|----------|
| 完整定位流程 | 1. 选择应用<br>2. 捕获元素<br>3. 生成代码<br>4. 测试定位 | 整个流程顺畅，定位成功 |
| 多应用类型支持 | 在不同类型应用上测试 | 支持MFC、WinForms、WPF、Qt应用 |
| 多定位方式 | 使用不同定位方式测试 | 所有定位方式都能成功定位元素 |
| 性能测试 | 在复杂UI上测试 | 元素捕获响应时间≤1秒，元素树加载时间≤3秒 |

## 7. 部署设计

### 7.1 安装包设计

采用PyInstaller进行打包，生成单文件可执行程序，支持离线安装。安装包包含以下内容：

- 主程序可执行文件
- 必要的依赖库
- 配置文件
- 帮助文档

### 7.2 安装流程

1. 运行安装程序
2. 选择安装目录
3. 点击"安装"按钮
4. 等待安装完成
5. 点击"完成"按钮，启动应用

### 7.3 卸载流程

1. 打开控制面板
2. 进入"程序和功能"
3. 找到Locator_desktop
4. 点击"卸载"
5. 按照提示完成卸载

## 8. 维护设计

### 8.1 日志设计

使用Python内置的logging模块，支持不同级别的日志记录，日志文件存储在用户目录下，便于问题排查和分析。

### 8.2 错误处理

采用异常捕获机制，对可能出现的异常进行捕获和处理，提供友好的错误信息，便于用户理解和解决问题。

### 8.3 版本控制

使用Git进行版本控制，遵循语义化版本规范，定期发布稳定版本，记录版本变更日志。

## 9. 优化与扩展

### 9.1 性能优化

- 实现元素树的异步加载，提高复杂UI的加载速度
- 优化图像识别算法，提高识别成功率和速度
- 实现元素缓存机制，减少重复捕获

### 9.2 功能扩展

- 支持更多自动化库的代码生成
- 实现元素定位历史记录功能
- 支持批量元素捕获和代码生成
- 提供定位代码导出功能
- 支持云端元素库管理

### 9.3 技术扩展

- 支持多语言界面
- 实现插件机制，支持功能扩展
- 提供API接口，支持与其他工具集成

## 10. 设计约束

| 约束类型 | 约束内容 | 影响范围 |
|----------|----------|----------|
| 技术约束 | 基于Windows平台 | 只能在Windows上运行 |
| 依赖约束 | 依赖pywinauto和uiautomation | 与这些库的兼容性有关 |
| 性能约束 | 复杂UI树加载时间≤3秒 | 元素分析模块 |
| 可用性约束 | 用户界面直观易用 | UI设计 |

## 11. 风险分析

| 风险点 | 影响程度 | 可能性 | 应对措施 |
|--------|----------|--------|----------|
| 外部依赖库更新 | 中 | 高 | 锁定依赖版本，定期测试兼容性 |
| 复杂UI树性能问题 | 中 | 高 | 实现异步加载和按需加载 |
| 某些应用类型不支持 | 中 | 中 | 提供替代定位方式，如图像识别 |
| 图像识别定位成功率低 | 中 | 中 | 优化图像识别算法，提供参数调整 |

## 12. 设计变更记录

| 版本 | 变更内容 | 变更时间 | 变更人 |
|------|----------|----------|--------|
| 1.0.0 | 初始设计 | 2025-12-18 | 开发团队 |

---

本设计文档详细描述了Locator_desktop的架构设计、模块设计、类设计、UI设计等内容，为开发和维护提供了详细的指导。