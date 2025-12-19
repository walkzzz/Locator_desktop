@echo off
setlocal enabledelayedexpansion

REM 设置日志文件
set LOG_FILE=build_log_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt

REM 日志函数
echo_log() {
    echo %* >> %LOG_FILE%
    echo %* 
}

REM 清理构建产物和缓存
clean_build() {
    echo_log "清理旧的构建产物和缓存..."
    echo_log "删除 build 目录..."
    rmdir /s /q build 2>nul
    echo_log "删除 dist 目录..."
    rmdir /s /q dist 2>nul
    echo_log "删除 .pytest_cache 目录..."
    rmdir /s /q .pytest_cache 2>nul
    echo_log "删除 __pycache__ 目录..."
    for /r %%i in (__pycache__) do rmdir /s /q "%%i" 2>nul
    echo_log "清理完成"
}

REM 初始化日志
echo. > %LOG_FILE%
echo_log =================================================
echo_log Locator_desktop 构建脚本
echo_log =================================================
echo_log 构建开始时间: %date% %time%
echo_log =================================================
echo_log.

REM 检查 Python 是否可用
echo_log 检查 Python 是否可用...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo_log 错误: 未找到 Python。请确保 Python 已安装并添加到 PATH。
    echo 错误: 未找到 Python。请确保 Python 已安装并添加到 PATH。
    pause
    exit /b 1
)
echo_log Python 版本:
python --version >> %LOG_FILE%
python --version

REM 检查 PyInstaller 是否可用
echo_log 检查 PyInstaller 是否可用...
python -c "import PyInstaller" >nul 2>nul
if %errorlevel% neq 0 (
    echo_log 安装 PyInstaller...
    pip install pyinstaller >> %LOG_FILE% 2>&1
    if %errorlevel% neq 0 (
        echo_log 错误: 安装 PyInstaller 失败。
        echo 错误: 安装 PyInstaller 失败。
        pause
        exit /b 1
    )
)
echo_log PyInstaller 版本:
python -c "import PyInstaller; print(PyInstaller.__version__)" >> %LOG_FILE%
python -c "import PyInstaller; print(PyInstaller.__version__)"

REM 创建输出目录
echo_log 创建输出目录...
mkdir -p dist

REM 构建选项菜单
echo.
echo 请选择构建类型:
echo 1. 单文件版本 (推荐用于快速使用)
echo 2. 便携版 (目录模式，解压即用)
echo 3. 同时构建两种版本
echo 4. 自动化构建 (默认: 同时构建两种版本)
echo.
set /p build_type="请输入选项 (1-4): "

REM 处理自动化构建选项
if "%build_type%" == "" set build_type=4
if "%build_type%" == "4" set build_type=3

REM 执行构建
echo_log.
echo_log 开始构建...
echo_log 构建类型: %build_type%
echo_log =================================================
echo.
echo 开始构建...
echo =================================================

REM 执行构建命令
set error_flag=0

if "%build_type%" == "1" (
    REM 构建单文件版本
    echo_log 构建单文件版本...
    python -m PyInstaller --onefile locator_desktop.spec >> %LOG_FILE% 2>&1
    if %errorlevel% neq 0 (
        echo_log 错误: 构建单文件版本失败。
        echo 错误: 构建单文件版本失败。查看 %LOG_FILE% 获取详细信息。
        set error_flag=1
    )
    
) else if "%build_type%" == "2" (
    REM 构建便携版
    echo_log 构建便携版...
    python -m PyInstaller --onedir locator_desktop.spec >> %LOG_FILE% 2>&1
    if %errorlevel% neq 0 (
        echo_log 错误: 构建便携版失败。
        echo 错误: 构建便携版失败。查看 %LOG_FILE% 获取详细信息。
        set error_flag=1
    )
    
) else if "%build_type%" == "3" (
    REM 同时构建两种版本
    echo_log 同时构建两种版本...
    python -m PyInstaller locator_desktop.spec >> %LOG_FILE% 2>&1
    if %errorlevel% neq 0 (
        echo_log 错误: 构建失败。
        echo 错误: 构建失败。查看 %LOG_FILE% 获取详细信息。
        set error_flag=1
    )
    
) else (
    echo_log 错误: 无效选项 %build_type%。
    echo 错误: 无效选项 %build_type%。
    set error_flag=1
)

REM 构建后验证
echo_log.
echo_log =================================================
echo_log 构建后验证...
echo_log =================================================

if %error_flag% equ 0 (
    REM 验证输出文件
    set validation_passed=1
    
    if "%build_type%" == "1" (
        REM 验证单文件版本
        if exist "dist\Locator_desktop.exe" (
            echo_log 单文件版本构建成功: dist\Locator_desktop.exe
            echo 单文件版本构建成功: dist\Locator_desktop.exe
        ) else (
            echo_log 错误: 单文件版本输出文件不存在
            echo 错误: 单文件版本输出文件不存在
            set validation_passed=0
        )
        
    ) else if "%build_type%" == "2" (
        REM 验证便携版
        if exist "dist\Locator_desktop_portable\Locator_desktop.exe" (
            echo_log 便携版构建成功: dist\Locator_desktop_portable\Locator_desktop.exe
            echo 便携版构建成功: dist\Locator_desktop_portable\Locator_desktop.exe
        ) else (
            echo_log 错误: 便携版输出文件不存在
            echo 错误: 便携版输出文件不存在
            set validation_passed=0
        )
        
    ) else if "%build_type%" == "3" (
        REM 验证两种版本
        if exist "dist\Locator_desktop.exe" (
            echo_log 单文件版本构建成功: dist\Locator_desktop.exe
            echo 单文件版本构建成功: dist\Locator_desktop.exe
        ) else (
            echo_log 错误: 单文件版本输出文件不存在
            echo 错误: 单文件版本输出文件不存在
            set validation_passed=0
        )
        
        if exist "dist\Locator_desktop_portable\Locator_desktop.exe" (
            echo_log 便携版构建成功: dist\Locator_desktop_portable\Locator_desktop.exe
            echo 便携版构建成功: dist\Locator_desktop_portable\Locator_desktop.exe
        ) else (
            echo_log 错误: 便携版输出文件不存在
            echo 错误: 便携版输出文件不存在
            set validation_passed=0
        )
    )
    
    if %validation_passed% equ 1 (
        echo_log.
        echo_log =================================================
        echo_log 构建完成！
        echo_log 输出目录: dist\
        echo_log.
        echo_log 运行说明:
        echo_log 1. 单文件版本: 直接运行 dist\Locator_desktop.exe
        echo_log 2. 便携版: 解压后运行 dist\Locator_desktop_portable\Locator_desktop.exe
        echo_log.
        echo_log 支持离线安装，无需额外依赖。
        echo_log 构建日志已保存到: %LOG_FILE%
        echo_log =================================================
        
        echo.
        echo =================================================
        echo 构建完成！
        echo 输出目录: dist\
        echo.
        echo 运行说明:
        echo 1. 单文件版本: 直接运行 dist\Locator_desktop.exe
        echo 2. 便携版: 解压后运行 dist\Locator_desktop_portable\Locator_desktop.exe
        echo.
        echo 支持离线安装，无需额外依赖。
        echo 构建日志已保存到: %LOG_FILE%
        echo =================================================
    ) else (
        echo_log.
        echo_log =================================================
        echo_log 构建完成，但验证失败！
        echo_log 请检查构建日志: %LOG_FILE%
        echo_log =================================================
        
        echo.
        echo =================================================
        echo 构建完成，但验证失败！
        echo 请检查构建日志: %LOG_FILE%
        echo =================================================
    )
) else (
    echo_log.
    echo_log =================================================
    echo_log 构建失败！
    echo_log 请检查构建日志: %LOG_FILE%
    echo_log =================================================
    
    echo.
    echo =================================================
    echo 构建失败！
    echo 请检查构建日志: %LOG_FILE%
    echo =================================================
)

REM 构建结束时间
echo_log.
echo_log =================================================
echo_log 构建结束时间: %date% %time%
echo_log =================================================

pause