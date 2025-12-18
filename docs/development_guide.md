# Locator_desktop 开发指南

## 1. 开发环境搭建

### 1.1 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 7 SP1、Windows 10、Windows 11 |
| Python版本 | Python 3.8或更高版本 |
| Git | Git 2.0或更高版本 |
| IDE | 推荐使用PyCharm或VS Code |

### 1.2 安装Python

1. 从[Python官网](https://www.python.org/downloads/)下载最新的Python 3.8+版本
2. 运行安装程序，勾选"Add Python to PATH"
3. 选择"Customize installation"，确保安装pip
4. 完成安装后，打开命令提示符验证安装：
   ```bash
   python --version
   pip --version
   ```

### 1.3 安装Git

1. 从[Git官网](https://git-scm.com/downloads)下载Git
2. 运行安装程序，按照默认选项安装
3. 完成安装后，打开命令提示符验证安装：
   ```bash
   git --version
   ```

### 1.4 克隆代码仓库

```bash
git clone https://github.com/locator-desktop/locator-desktop.git
cd locator-desktop
```

### 1.5 创建虚拟环境

#### 使用venv

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows CMD
venv\Scripts\activate.bat
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

#### 使用conda

```bash
# 创建虚拟环境
conda create -n locator-desktop python=3.8

# 激活虚拟环境
conda activate locator-desktop
```

### 1.6 安装依赖

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 或安装生产依赖
pip install -r requirements.txt
```

## 2. 项目结构

```
LocatorProject/
├── src/                    # 源代码目录
│   ├── main.py              # 应用入口
│   ├── ui/                  # UI相关代码
│   │   └── main_window.py   # 主窗口UI实现
│   ├── core/                # 核心业务逻辑
│   │   ├── element.py          # 元素数据结构
│   │   ├── element_capture.py  # 元素捕获逻辑
│   │   ├── element_analyzer.py # 元素分析模块
│   │   └── code_generator.py   # 定位代码生成器
│   ├── utils/               # 工具函数
│   │   ├── window_utils.py     # 窗口管理工具
│   │   └── process_utils.py    # 进程管理工具
│   └── resources/           # 资源文件
├── docs/                    # 文档目录
│   ├── requirements.md        # 需求文档
│   ├── design.md              # 设计文档
│   ├── api.md                 # API文档
│   ├── user_manual.md         # 用户手册
│   └── development_guide.md   # 开发指南
├── tests/                   # 测试代码
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   └── system/                # 系统测试
├── requirements.txt         # 生产依赖
├── requirements-dev.txt     # 开发依赖
├── setup.py                 # 打包配置
├── .gitignore               # Git忽略文件
└── README.md                # 项目说明
```

### 2.1 模块说明

| 模块 | 主要职责 | 文件位置 |
|------|----------|----------|
| 应用入口 | 启动应用程序 | src/main.py |
| 主窗口UI | 实现应用主界面 | src/ui/main_window.py |
| 元素数据结构 | 定义元素属性和行为 | src/core/element.py |
| 元素捕获 | 捕获和识别UI元素 | src/core/element_capture.py |
| 元素分析 | 分析元素结构和属性 | src/core/element_analyzer.py |
| 代码生成 | 生成定位代码 | src/core/code_generator.py |
| 窗口工具 | 窗口管理和操作 | src/utils/window_utils.py |
| 进程工具 | 进程管理和操作 | src/utils/process_utils.py |

## 3. 开发流程

### 3.1 分支管理

项目采用Git Flow分支管理策略：

- **main**：主分支，用于发布稳定版本
- **develop**：开发分支，用于集成新功能
- **feature/xxx**：功能分支，用于开发新功能
- **bugfix/xxx**：修复分支，用于修复bug
- **release/xxx**：发布分支，用于准备发布版本

### 3.2 开发步骤

1. **更新代码**：
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **创建分支**：
   ```bash
   # 开发新功能
   git checkout -b feature/your-feature-name
   
   # 修复bug
   git checkout -b bugfix/your-bugfix-name
   ```

3. **编写代码**：
   - 遵循代码规范
   - 编写单元测试
   - 确保代码覆盖率

4. **运行测试**：
   ```bash
   pytest tests/unit/ -v
   ```

5. **提交代码**：
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

6. **推送分支**：
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**：
   - 从feature分支向develop分支创建PR
   - 填写PR描述，包括功能说明和测试结果
   - 等待代码审查

8. **合并代码**：
   - 代码审查通过后，合并到develop分支
   - 删除功能分支

### 3.3 代码审查规范

- 代码必须符合项目的代码规范
- 必须包含单元测试
- 代码覆盖率不低于80%
- 提交信息清晰明了
- PR描述详细，包含功能说明和测试结果

## 4. 代码规范

### 4.1 Python代码规范

- 遵循PEP 8规范
- 使用4个空格缩进
- 每行不超过100个字符
- 变量和函数名使用小写字母和下划线
- 类名使用驼峰命名法
- 常量使用全大写字母和下划线
- 导入顺序：标准库 → 第三方库 → 本地库
- 函数和方法必须有文档字符串
- 类必须有类文档字符串

### 4.2 文档字符串规范

使用Google风格的文档字符串：

```python
def function_name(param1, param2):
    """函数功能描述
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
        
    Returns:
        返回值的描述
        
    Raises:
        ExceptionType: 异常说明
    """
    pass
```

### 4.3 命名规范

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 变量 | 小写字母+下划线 | `element_name` |
| 函数 | 小写字母+下划线 | `capture_element()` |
| 类 | 驼峰命名法 | `ElementCapture` |
| 常量 | 全大写+下划线 | `MAX_DEPTH` |
| 模块 | 小写字母+下划线 | `element_capture.py` |
| 包 | 小写字母 | `core` |

## 5. 测试方法

### 5.1 测试框架

- **单元测试**：使用pytest
- **集成测试**：使用pytest
- **系统测试**：使用pytest结合pywinauto

### 5.2 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/ -v

# 运行集成测试
pytest tests/integration/ -v

# 运行系统测试
pytest tests/system/ -v

# 生成测试报告
pytest --cov=src --cov-report=html
```

### 5.3 测试覆盖率

- 目标覆盖率：80%
- 使用pytest-cov生成覆盖率报告
- 覆盖率报告位置：`htmlcov/index.html`

### 5.4 编写测试

#### 单元测试示例

```python
# tests/unit/test_element.py
import pytest
from core.element import Element

def test_element_creation():
    """测试元素创建"""
    element = Element()
    assert element is not None
    assert element.name is None
    assert element.children == []

def test_add_child():
    """测试添加子元素"""
    parent = Element()
    child = Element()
    parent.add_child(child)
    
    assert len(parent.children) == 1
    assert child.parent == parent
    assert child.depth == 1
```

#### 集成测试示例

```python
# tests/integration/test_element_capture.py
import pytest
from core.element_capture import ElementCapture
from utils.window_utils import WindowUtils

def test_capture_element():
    """测试元素捕获功能"""
    # 准备：打开记事本
    import subprocess
    subprocess.Popen("notepad.exe")
    time.sleep(1)  # 等待记事本启动
    
    # 获取记事本窗口
    window = WindowUtils.get_window_by_title("无标题 - 记事本")
    assert window is not None
    
    # 测试捕获元素
    capture = ElementCapture()
    # 这里需要模拟鼠标操作，实际测试中可以使用pywinauto模拟
    # element = capture.capture_element()
    # assert element is not None
    
    # 清理：关闭记事本
    window.close()
```

## 6. 调试技巧

### 6.1 使用PyCharm调试

1. 打开项目文件夹
2. 设置断点
3. 选择"Run" → "Debug 'main'"
4. 使用调试工具查看变量和执行流程

### 6.2 使用VS Code调试

1. 安装Python扩展
2. 配置launch.json：
   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Main",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}/src/main.py",
               "console": "integratedTerminal"
           }
       ]
   }
   ```
3. 设置断点
4. 按F5启动调试

### 6.3 使用日志调试

```python
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 在代码中添加日志
logger.debug(f"Element properties: {element.__dict__}")
logger.info(f"Captured element: {element}")
logger.error(f"Failed to capture element: {e}")
```

## 7. 打包部署

### 7.1 打包工具

项目使用PyInstaller进行打包，支持以下打包方式：

- 单文件可执行程序
- 目录打包
- 支持离线安装

### 7.2 打包步骤

1. **安装PyInstaller**：
   ```bash
   pip install pyinstaller
   ```

2. **打包为单文件**：
   ```bash
   pyinstaller --onefile --windowed src/main.py
   ```

3. **打包为目录**：
   ```bash
   pyinstaller --windowed src/main.py
   ```

4. **自定义打包配置**：
   ```bash
   pyinstaller main.spec
   ```

### 7.3 打包配置

`main.spec`文件示例：

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['src/main.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=['pywinauto', 'uiautomation'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

ex = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Locator_desktop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
```

### 7.4 离线安装包制作

使用NSIS或Inno Setup制作离线安装包：

1. **NSIS**：
   - 下载并安装NSIS
   - 编写NSIS脚本
   - 编译生成安装包

2. **Inno Setup**：
   - 下载并安装Inno Setup
   - 编写Inno Setup脚本
   - 编译生成安装包

### 7.5 发布版本

1. **更新版本号**：
   - 修改`setup.py`中的版本号
   - 更新`__version__`变量

2. **生成发布包**：
   ```bash
   python setup.py sdist bdist_wheel
   ```

3. **上传到PyPI**：
   ```bash
   twine upload dist/*
   ```

## 8. 代码质量

### 8.1 代码检查

使用以下工具进行代码检查：

```bash
# 使用flake8检查代码风格
flake8 src/

# 使用pylint检查代码质量
pylint src/

# 使用black格式化代码
black src/

# 使用isort排序导入
isort src/
```

### 8.2 类型检查

使用mypy进行类型检查：

```bash
mypy src/
```

## 9. 贡献指南

### 9.1 提交代码

1. **遵循Git Flow分支策略**
2. **编写清晰的提交信息**
3. **确保代码通过所有测试**
4. **确保代码覆盖率达标**
5. **提交PR时填写详细描述**

### 9.2 提交信息规范

使用以下格式编写提交信息：

```
Type: Subject

Body (optional)
```

**Type**可选值：
- `Add`：添加新功能
- `Fix`：修复bug
- `Update`：更新功能
- `Refactor`：重构代码
- `Docs`：更新文档
- `Test`：添加或更新测试
- `Chore`：杂项更改（如配置文件）

**示例**：
```
Add: 实现元素捕获功能

- 添加ElementCapture类
- 实现鼠标悬停捕获
- 支持多种定位方式
```

### 9.3 报告问题

在GitHub Issues中报告问题时，请包含以下信息：

- 问题描述
- 重现步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、Python版本、Locator_desktop版本）
- 错误日志

## 10. 常见问题

### 10.1 安装依赖失败

**问题**：安装依赖时出现"ModuleNotFoundError"

**解决方案**：
- 确保Python版本符合要求
- 确保虚拟环境已激活
- 尝试使用国内镜像源：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
  ```

### 10.2 应用启动失败

**问题**：运行`python src/main.py`时出现错误

**解决方案**：
- 检查依赖是否安装完整
- 检查Python版本是否符合要求
- 查看错误日志，定位具体问题
- 尝试重新安装依赖

### 10.3 测试失败

**问题**：运行测试时出现失败

**解决方案**：
- 检查测试环境是否正确设置
- 查看测试失败信息，定位问题
- 确保测试依赖已安装
- 尝试单独运行失败的测试：
  ```bash
  pytest tests/unit/test_element.py::test_element_creation -v
  ```

### 10.4 打包失败

**问题**：使用PyInstaller打包时出现错误

**解决方案**：
- 确保所有依赖已安装
- 检查`main.spec`配置是否正确
- 尝试添加缺失的hiddenimports
- 查看PyInstaller日志，定位具体问题

## 11. 技术栈说明

| 技术/库 | 用途 | 版本要求 |
|---------|------|----------|
| Python | 编程语言 | 3.8+ |
| PyQt5 | GUI框架 | 5.15.0+ |
| pywinauto | Windows自动化 | 0.6.8+ |
| uiautomation | UI自动化 | 2.0.11+ |
| opencv-python | 图像识别 | 4.5.0+ |
| pillow | 图像处理 | 8.0.0+ |
| pygetwindow | 窗口管理 | 0.0.9+ |
| psutil | 进程管理 | 5.8.0+ |
| pytest | 测试框架 | 6.0.0+ |
| flake8 | 代码检查 | 3.8.0+ |
| pylint | 代码质量 | 2.6.0+ |
| black | 代码格式化 | 21.0.0+ |
| mypy | 类型检查 | 0.800+ |
| PyInstaller | 打包工具 | 4.0+ |

## 12. 开发工具推荐

### 12.1 IDE

- **PyCharm**：专业的Python IDE，推荐使用Professional版本
- **VS Code**：轻量级编辑器，安装Python扩展后使用
- **Sublime Text**：轻量级编辑器，适合快速编辑

### 12.2 插件推荐

**PyCharm插件**：
- Python
- Qt Designer Integration
- CodeGlance
- GitToolBox
- Material Theme UI

**VS Code插件**：
- Python
- Pylance
- Code Runner
- GitLens
- Material Icon Theme

## 13. 后续开发计划

### 13.1 短期计划

- [ ] 完善元素捕获功能
- [ ] 优化图像识别算法
- [ ] 增加定位代码导出功能
- [ ] 实现元素定位历史记录

### 13.2 长期计划

- [ ] 支持更多自动化库
- [ ] 实现批量元素捕获
- [ ] 支持云端元素库管理
- [ ] 开发插件系统
- [ ] 支持多语言界面

## 14. 联系方式

- **项目地址**：[GitHub Repository](https://github.com/locator-desktop/locator-desktop)
- **Issue跟踪**：[GitHub Issues](https://github.com/locator-desktop/locator-desktop/issues)
- **讨论区**：[GitHub Discussions](https://github.com/locator-desktop/locator-desktop/discussions)
- **邮箱**：dev@locator-desktop.com

## 15. 许可协议

Locator_desktop采用MIT许可证，详情见LICENSE文件。

---

感谢您对Locator_desktop项目的贡献！