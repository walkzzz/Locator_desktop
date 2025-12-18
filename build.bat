@echo off
setlocal enabledelayedexpansion

echo =================================================
echo Locator_desktop 构建脚本
echo =================================================
echo.

REM 检查 Python 是否可用
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python。请确保 Python 已安装并添加到 PATH。
    pause
    exit /b 1
)

REM 检查 PyInstaller 是否可用
python -c "import PyInstaller" >nul 2>nul
if %errorlevel% neq 0 (
    echo 安装 PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo 错误: 安装 PyInstaller 失败。
        pause
        exit /b 1
    )
)

REM 创建输出目录
mkdir -p dist

REM 构建选项菜单
echo 请选择构建类型:
echo 1. 单文件版本 (推荐用于快速使用)
echo 2. 便携版 (目录模式，解压即用)
echo 3. 同时构建两种版本
echo.
set /p build_type="请输入选项 (1-3): "

REM 执行构建
echo.
echo 开始构建...
echo =================================================

if "%build_type%" == "1" (
    REM 构建单文件版本
    python -m PyInstaller --onefile locator_desktop.spec
    if %errorlevel% neq 0 (
        echo 错误: 构建单文件版本失败。
        pause
        exit /b 1
    )
    echo 单文件版本构建完成: dist\Locator_desktop.exe
    
) else if "%build_type%" == "2" (
    REM 构建便携版
    python -m PyInstaller --onedir locator_desktop.spec
    if %errorlevel% neq 0 (
        echo 错误: 构建便携版失败。
        pause
        exit /b 1
    )
    echo 便携版构建完成: dist\Locator_desktop_portable\
    
) else if "%build_type%" == "3" (
    REM 同时构建两种版本
    python -m PyInstaller locator_desktop.spec
    if %errorlevel% neq 0 (
        echo 错误: 构建失败。
        pause
        exit /b 1
    )
    echo 单文件版本构建完成: dist\Locator_desktop.exe
    echo 便携版构建完成: dist\Locator_desktop_portable\
    
) else (
    echo 错误: 无效选项。
    pause
    exit /b 1
)

echo =================================================
echo 构建完成！
echo 输出目录: dist\
echo.
echo 运行说明:
echo 1. 单文件版本: 直接运行 dist\Locator_desktop.exe
echo 2. 便携版: 解压后运行 dist\Locator_desktop_portable\Locator_desktop.exe
echo.
echo 支持离线安装，无需额外依赖。
echo =================================================
pause