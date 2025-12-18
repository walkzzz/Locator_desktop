#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QGridLayout,
    QTabWidget, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from core.element_capture import ElementCapture
from core.element_analyzer import ElementAnalyzer
from core.code_generator import CodeGenerator
from utils.window_utils import WindowUtils
from utils.process_utils import ProcessUtils


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Locator_desktop - 桌面应用元素定位工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化核心模块
        self.element_capture = ElementCapture()
        self.element_analyzer = ElementAnalyzer()
        self.code_generator = CodeGenerator()
        self.window_utils = WindowUtils()
        self.process_utils = ProcessUtils()
        
        # 当前选中的元素
        self.current_element = None
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号与槽
        self.connect_signals()
        
        # 初始化应用列表
        self.refresh_process_list()
    
    def init_ui(self):
        """初始化UI布局"""
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # 主分割器
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # 左侧面板：应用选择和元素树
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右侧分割器
        right_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(right_splitter)
        
        # 右侧上方面板：元素详细信息
        right_top_panel = self.create_right_top_panel()
        right_splitter.addWidget(right_top_panel)
        
        # 右侧下方面板：定位代码生成
        right_bottom_panel = self.create_right_bottom_panel()
        right_splitter.addWidget(right_bottom_panel)
        
        # 设置分割器比例
        main_splitter.setSizes([400, 800])
        right_splitter.setSizes([400, 400])
    
    def create_toolbar(self):
        """创建顶部工具栏"""
        toolbar = QGroupBox("应用程序选择")
        layout = QHBoxLayout()
        
        # 应用路径输入
        self.app_path_edit = QLineEdit()
        self.app_path_edit.setPlaceholderText("请输入应用程序路径或拖拽应用到此处")
        layout.addWidget(QLabel("应用程序:"))
        layout.addWidget(self.app_path_edit)
        
        # 查找按钮
        self.find_next_btn = QPushButton("查找下一个")
        self.find_prev_btn = QPushButton("查找上一个")
        layout.addWidget(self.find_next_btn)
        layout.addWidget(self.find_prev_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        layout.addWidget(self.refresh_btn)
        
        # 捕获按钮
        self.capture_btn = QPushButton("捕获元素")
        self.capture_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        layout.addWidget(self.capture_btn)
        
        toolbar.setLayout(layout)
        return toolbar
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 元素树
        self.element_tree = QTreeWidget()
        self.element_tree.setHeaderLabel("元素树")
        self.element_tree.setColumnCount(1)
        layout.addWidget(self.element_tree)
        
        return panel
    
    def create_right_top_panel(self):
        """创建右侧上方面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 左侧：元素详细信息
        info_group = QGroupBox("元素详细信息")
        info_layout = QVBoxLayout()
        
        # 元素信息表格
        self.element_info_table = QTableWidget(10, 2)
        self.element_info_table.setHorizontalHeaderLabels(["属性名", "属性值"])
        self.element_info_table.horizontalHeader().setStretchLastSection(True)
        info_layout.addWidget(self.element_info_table)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 右侧：定位路径
        path_group = QGroupBox("定位路径")
        path_layout = QVBoxLayout()
        
        self.path_text_edit = QTextEdit()
        self.path_text_edit.setReadOnly(True)
        path_layout.addWidget(self.path_text_edit)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        return panel
    
    def create_right_bottom_panel(self):
        """创建右侧下方面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 定位方式选择
        locate_method_group = QGroupBox("定位方式")
        locate_method_layout = QHBoxLayout()
        
        self.method_group = QButtonGroup()
        
        self.attr_radio = QRadioButton("属性定位")
        self.attr_radio.setChecked(True)
        self.image_radio = QRadioButton("图像识别")
        self.coord_radio = QRadioButton("坐标定位")
        
        self.method_group.addButton(self.attr_radio)
        self.method_group.addButton(self.image_radio)
        self.method_group.addButton(self.coord_radio)
        
        locate_method_layout.addWidget(self.attr_radio)
        locate_method_layout.addWidget(self.image_radio)
        locate_method_layout.addWidget(self.coord_radio)
        
        locate_method_group.setLayout(locate_method_layout)
        layout.addWidget(locate_method_group)
        
        # 定位代码生成
        code_group = QGroupBox("定位代码生成")
        code_layout = QVBoxLayout()
        
        # 标签页：支持不同库的代码生成
        self.code_tab = QTabWidget()
        
        # pywinauto代码
        self.pywinauto_code_edit = QTextEdit()
        self.pywinauto_code_edit.setReadOnly(True)
        self.pywinauto_code_edit.setFont(QFont("Consolas", 10))
        self.code_tab.addTab(self.pywinauto_code_edit, "pywinauto")
        
        # uiautomation代码
        self.uiauto_code_edit = QTextEdit()
        self.uiauto_code_edit.setReadOnly(True)
        self.uiauto_code_edit.setFont(QFont("Consolas", 10))
        self.code_tab.addTab(self.uiauto_code_edit, "uiautomation")
        
        code_layout.addWidget(self.code_tab)
        
        # 测试按钮
        test_layout = QHBoxLayout()
        self.test_loc_btn = QPushButton("测试定位")
        self.copy_btn = QPushButton("复制代码")
        test_layout.addWidget(self.test_loc_btn)
        test_layout.addWidget(self.copy_btn)
        code_layout.addLayout(test_layout)
        
        code_group.setLayout(code_layout)
        layout.addWidget(code_group)
        
        return panel
    
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 应用进程选择
        process_group = QGroupBox("进程选择")
        process_layout = QVBoxLayout()
        
        self.process_combo = QComboBox()
        process_layout.addWidget(self.process_combo)
        
        # 窗口选择
        self.window_combo = QComboBox()
        process_layout.addWidget(QLabel("窗口:"))
        process_layout.addWidget(self.window_combo)
        
        process_group.setLayout(process_layout)
        layout.addWidget(process_group)
        
        # 元素树
        element_tree_group = QGroupBox("元素树")
        element_tree_layout = QVBoxLayout()
        
        self.element_tree = QTreeWidget()
        self.element_tree.setHeaderLabel("元素")
        self.element_tree.setColumnCount(1)
        element_tree_layout.addWidget(self.element_tree)
        
        element_tree_group.setLayout(element_tree_layout)
        layout.addWidget(element_tree_group)
        
        return panel
    
    def connect_signals(self):
        """连接信号与槽"""
        # 进程选择变化
        self.process_combo.currentIndexChanged.connect(self.on_process_changed)
        
        # 窗口选择变化
        self.window_combo.currentIndexChanged.connect(self.on_window_changed)
        
        # 元素树选择变化
        self.element_tree.itemClicked.connect(self.on_element_selected)
        
        # 按钮点击事件
        self.refresh_btn.clicked.connect(self.refresh_process_list)
        self.capture_btn.clicked.connect(self.start_capture)
        self.test_loc_btn.clicked.connect(self.test_location)
        self.copy_btn.clicked.connect(self.copy_code)
    
    def refresh_process_list(self):
        """刷新进程列表"""
        processes = self.process_utils.get_running_processes()
        self.process_combo.clear()
        for process in processes:
            self.process_combo.addItem(f"{process.name} (PID: {process.pid})")
    
    def on_process_changed(self):
        """进程选择变化时的处理"""
        # 更新窗口列表
        processes = self.process_utils.get_running_processes()
        if self.process_combo.currentIndex() < len(processes):
            process = processes[self.process_combo.currentIndex()]
            windows = self.window_utils.get_windows_by_pid(process.pid)
            self.window_combo.clear()
            for window in windows:
                self.window_combo.addItem(window.title)
    
    def on_window_changed(self):
        """窗口选择变化时的处理"""
        # 更新元素树
        self.update_element_tree()
    
    def update_element_tree(self):
        """更新元素树"""
        # 清空当前元素树
        self.element_tree.clear()
        
        # 获取当前选择的窗口
        window_title = self.window_combo.currentText()
        if not window_title:
            return
        
        # 获取窗口句柄
        window = self.window_utils.get_window_by_title(window_title)
        if not window:
            return
        
        # 构建元素树
        root_element = self.element_analyzer.analyze_window(window)
        if root_element:
            self.build_element_tree(root_element)
    
    def build_element_tree(self, element, parent_item=None):
        """构建元素树"""
        if parent_item is None:
            parent_item = self.element_tree.invisibleRootItem()
        
        # 创建树节点
        item = QTreeWidgetItem(parent_item)
        item.setText(0, f"{element.element_type} - {element.name or ''}")
        item.setData(0, Qt.UserRole, element)
        
        # 递归添加子元素
        for child in element.children:
            self.build_element_tree(child, item)
    
    def on_element_selected(self, item, column):
        """元素树节点选中时的处理"""
        element = item.data(0, Qt.UserRole)
        if not element:
            return
        
        self.current_element = element
        
        # 更新元素详细信息
        self.update_element_info(element)
        
        # 更新定位路径
        self.update_element_path(element)
        
        # 生成定位代码
        self.generate_locator_code(element)
    
    def update_element_info(self, element):
        """更新元素详细信息"""
        self.element_info_table.setRowCount(0)
        
        # 元素属性列表
        properties = [
            ("元素ID", element.element_id),
            ("元素名称", element.name),
            ("元素类型", element.element_type),
            ("元素坐标", f"({element.x}, {element.y})") if element.x and element.y else ("元素坐标", ""),
            ("元素尺寸", f"({element.width}x{element.height})") if element.width and element.height else ("元素尺寸", ""),
            ("AutomationID", element.automation_id),
            ("ClassName", element.class_name),
            ("ControlType", element.control_type),
            ("Depth", element.depth),
        ]
        
        # 填充表格
        for row, (key, value) in enumerate(properties):
            self.element_info_table.insertRow(row)
            self.element_info_table.setItem(row, 0, QTableWidgetItem(key))
            self.element_info_table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def update_element_path(self, element):
        """更新元素路径"""
        path = self.element_analyzer.get_element_path(element)
        self.path_text_edit.setPlainText(path)
    
    def generate_locator_code(self, element):
        """生成定位代码"""
        # 生成pywinauto代码
        pywinauto_code = self.code_generator.generate_pywinauto_code(element)
        self.pywinauto_code_edit.setPlainText(pywinauto_code)
        
        # 生成uiautomation代码
        uiauto_code = self.code_generator.generate_uiautomation_code(element)
        self.uiauto_code_edit.setPlainText(uiauto_code)
    
    def start_capture(self):
        """开始捕获元素"""
        self.capture_btn.setText("捕获中...")
        self.capture_btn.setEnabled(False)
        
        # 调用元素捕获模块
        element = self.element_capture.capture_element()
        
        if element:
            # 更新当前元素
            self.current_element = element
            
            # 更新UI
            self.update_element_info(element)
            self.update_element_path(element)
            self.generate_locator_code(element)
            
            # 在元素树中选中该元素
            self.select_element_in_tree(element)
        
        self.capture_btn.setText("捕获元素")
        self.capture_btn.setEnabled(True)
    
    def select_element_in_tree(self, target_element):
        """在元素树中选中目标元素"""
        def find_element(item):
            element = item.data(0, Qt.UserRole)
            if element == target_element:
                return item
            for i in range(item.childCount()):
                child_item = item.child(i)
                found = find_element(child_item)
                if found:
                    return found
            return None
        
        root_item = self.element_tree.invisibleRootItem()
        found_item = find_element(root_item)
        if found_item:
            self.element_tree.setCurrentItem(found_item)
    
    def test_location(self):
        """测试定位代码"""
        if not self.current_element:
            QMessageBox.warning(self, "警告", "请先选择或捕获一个元素")
            return
        
        # 测试定位
        result = self.element_capture.test_element_location(self.current_element)
        if result:
            QMessageBox.information(self, "成功", "定位成功！")
        else:
            QMessageBox.warning(self, "失败", "定位失败，请检查定位表达式")
    
    def copy_code(self):
        """复制当前选中标签页的代码"""
        current_tab = self.code_tab.currentIndex()
        if current_tab == 0:
            code = self.pywinauto_code_edit.toPlainText()
        else:
            code = self.uiauto_code_edit.toPlainText()
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        QMessageBox.information(self, "成功", "代码已复制到剪贴板")
    
    def on_process_changed(self):
        """进程选择变化时的处理"""
        # 更新窗口列表
        current_text = self.process_combo.currentText()
        if current_text:
            # 提取PID
            pid_str = current_text.split("(PID: ")[-1].rstrip(")")
            try:
                pid = int(pid_str)
                windows = self.window_utils.get_windows_by_pid(pid)
                self.window_combo.clear()
                for window in windows:
                    self.window_combo.addItem(window.title)
            except ValueError:
                pass
    
    def on_window_changed(self):
        """窗口选择变化时的处理"""
        # 更新元素树
        self.update_element_tree()
