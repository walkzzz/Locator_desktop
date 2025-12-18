#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QGridLayout,
    QTabWidget, QRadioButton, QButtonGroup, QMessageBox, QFileDialog,
    QWizard, QWizardPage, QVBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from core.element_capture import ElementCapture
from core.element_analyzer import ElementAnalyzer
from core.code_generator import CodeGenerator
from core.history_manager import HistoryManager
from core.favorites_manager import FavoritesManager
from core.plugin_manager import PluginManager
from core.api_service import APIService
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
        self.history_manager = HistoryManager()
        self.favorites_manager = FavoritesManager()
        self.plugin_manager = PluginManager()
        
        # 加载和初始化插件
        self.plugin_manager.load_plugins()
        self.plugin_manager.initialize_plugins(self)
        
        # 初始化API服务
        self.api_service = APIService(self)
        
        # 启动API服务
        self.api_service.start()
        self.update_status("API服务已启动，端口: 5000")
        
        # 当前选中的元素
        self.current_element = None
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号与槽
        self.connect_signals()
        
        # 初始化应用列表
        self.refresh_process_list()
        
        # 初始化历史记录
        self.refresh_history_list()
        
        # 初始化收藏夹
        self.refresh_favorites_list()
    
    def init_ui(self):
        """初始化UI布局"""
        # 设置状态栏
        self.statusBar().showMessage("就绪")
        
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # 添加向导式操作按钮
        wizard_layout = QHBoxLayout()
        self.wizard_btn = QPushButton("启动向导")
        self.wizard_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        wizard_layout.addWidget(self.wizard_btn)
        wizard_layout.addStretch()
        main_layout.addLayout(wizard_layout)
        
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
        
        # 创建向导对话框
        self.create_wizard_dialog()
        
        # 初始化日志记录
        self.init_logging()
    
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
        
        # 主标签页：代码生成和历史记录
        self.main_tab = QTabWidget()
        layout.addWidget(self.main_tab)
        
        # 代码生成标签页
        code_tab_widget = QWidget()
        code_tab_layout = QVBoxLayout(code_tab_widget)
        
        # 定位方式选择
        locate_method_group = QGroupBox("定位方式")
        locate_method_layout = QVBoxLayout()
        
        # 快捷按钮区域
        quick_method_layout = QHBoxLayout()
        
        # 属性定位快捷按钮
        self.attr_btn = QPushButton("属性定位")
        self.attr_btn.setCheckable(True)
        self.attr_btn.setChecked(True)
        quick_method_layout.addWidget(self.attr_btn)
        
        # 图像识别快捷按钮
        self.image_btn = QPushButton("图像识别")
        self.image_btn.setCheckable(True)
        quick_method_layout.addWidget(self.image_btn)
        
        # 坐标定位快捷按钮
        self.coord_btn = QPushButton("坐标定位")
        self.coord_btn.setCheckable(True)
        quick_method_layout.addWidget(self.coord_btn)
        
        # pyautogui快捷按钮
        self.pyautogui_btn = QPushButton("PyAutoGUI")
        self.pyautogui_btn.setCheckable(True)
        quick_method_layout.addWidget(self.pyautogui_btn)
        
        # win32gui快捷按钮
        self.win32gui_btn = QPushButton("Win32GUI")
        self.win32gui_btn.setCheckable(True)
        quick_method_layout.addWidget(self.win32gui_btn)
        
        # 添加快捷按钮到布局
        locate_method_layout.addLayout(quick_method_layout)
        
        # 按钮组，确保只有一个按钮被选中
        self.method_btn_group = QButtonGroup()
        self.method_btn_group.setExclusive(True)
        self.method_btn_group.addButton(self.attr_btn)
        self.method_btn_group.addButton(self.image_btn)
        self.method_btn_group.addButton(self.coord_btn)
        self.method_btn_group.addButton(self.pyautogui_btn)
        self.method_btn_group.addButton(self.win32gui_btn)
        
        # 传统单选按钮（保持兼容性）
        traditional_method_layout = QHBoxLayout()
        self.method_group = QButtonGroup()
        
        self.attr_radio = QRadioButton("属性定位")
        self.attr_radio.setChecked(True)
        self.image_radio = QRadioButton("图像识别")
        self.coord_radio = QRadioButton("坐标定位")
        
        self.method_group.addButton(self.attr_radio)
        self.method_group.addButton(self.image_radio)
        self.method_group.addButton(self.coord_radio)
        
        traditional_method_layout.addWidget(self.attr_radio)
        traditional_method_layout.addWidget(self.image_radio)
        traditional_method_layout.addWidget(self.coord_radio)
        traditional_method_layout.addStretch()
        
        # 添加传统单选按钮到布局
        locate_method_layout.addLayout(traditional_method_layout)
        
        locate_method_group.setLayout(locate_method_layout)
        code_tab_layout.addWidget(locate_method_group)
        
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
        self.export_btn = QPushButton("导出代码")
        test_layout.addWidget(self.test_loc_btn)
        test_layout.addWidget(self.copy_btn)
        test_layout.addWidget(self.export_btn)
        code_layout.addLayout(test_layout)
        
        code_group.setLayout(code_layout)
        code_tab_layout.addWidget(code_group)
        
        # 历史记录标签页
        history_tab_widget = QWidget()
        history_tab_layout = QVBoxLayout(history_tab_widget)
        
        # 历史记录搜索和管理
        history_control_layout = QHBoxLayout()
        
        self.history_search_edit = QLineEdit()
        self.history_search_edit.setPlaceholderText("搜索历史记录...")
        self.history_search_btn = QPushButton("搜索")
        self.history_clear_btn = QPushButton("清空")
        
        history_control_layout.addWidget(self.history_search_edit)
        history_control_layout.addWidget(self.history_search_btn)
        history_control_layout.addWidget(self.history_clear_btn)
        
        history_tab_layout.addLayout(history_control_layout)
        
        # 历史记录列表
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "时间", "应用", "元素类型", "定位方法"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        history_tab_layout.addWidget(self.history_table)
        
        # 历史记录操作
        history_action_layout = QHBoxLayout()
        self.history_detail_btn = QPushButton("查看详情")
        self.history_delete_btn = QPushButton("删除记录")
        history_action_layout.addWidget(self.history_detail_btn)
        history_action_layout.addWidget(self.history_delete_btn)
        history_tab_layout.addLayout(history_action_layout)
        
        # 收藏夹标签页
        favorites_tab_widget = QWidget()
        favorites_tab_layout = QVBoxLayout(favorites_tab_widget)
        
        # 收藏夹搜索和管理
        favorites_control_layout = QHBoxLayout()
        
        self.favorites_search_edit = QLineEdit()
        self.favorites_search_edit.setPlaceholderText("搜索收藏夹...")
        self.favorites_search_btn = QPushButton("搜索")
        self.favorites_refresh_btn = QPushButton("刷新")
        
        favorites_control_layout.addWidget(self.favorites_search_edit)
        favorites_control_layout.addWidget(self.favorites_search_btn)
        favorites_control_layout.addWidget(self.favorites_refresh_btn)
        
        favorites_tab_layout.addLayout(favorites_control_layout)
        
        # 收藏夹列表
        self.favorites_table = QTableWidget()
        self.favorites_table.setColumnCount(4)
        self.favorites_table.setHorizontalHeaderLabels(["ID", "元素类型", "元素名称", "标签"])
        self.favorites_table.horizontalHeader().setStretchLastSection(True)
        favorites_tab_layout.addWidget(self.favorites_table)
        
        # 收藏夹操作
        favorites_action_layout = QHBoxLayout()
        self.add_favorite_btn = QPushButton("添加到收藏夹")
        self.remove_favorite_btn = QPushButton("移除收藏")
        self.favorite_detail_btn = QPushButton("查看详情")
        favorites_action_layout.addWidget(self.add_favorite_btn)
        favorites_action_layout.addWidget(self.remove_favorite_btn)
        favorites_action_layout.addWidget(self.favorite_detail_btn)
        favorites_tab_layout.addLayout(favorites_action_layout)
        
        # 添加标签页到主标签页
        self.main_tab.addTab(code_tab_widget, "代码生成")
        self.main_tab.addTab(history_tab_widget, "历史记录")
        self.main_tab.addTab(favorites_tab_widget, "收藏夹")
        
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
        
        # 元素树搜索框
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))
        self.element_search_edit = QLineEdit()
        self.element_search_edit.setPlaceholderText("按元素名称或类型搜索")
        search_layout.addWidget(self.element_search_edit)
        self.element_search_btn = QPushButton("搜索")
        search_layout.addWidget(self.element_search_btn)
        element_tree_layout.addLayout(search_layout)
        
        # 元素树
        self.element_tree = QTreeWidget()
        self.element_tree.setHeaderLabel("元素")
        self.element_tree.setColumnCount(1)
        element_tree_layout.addWidget(self.element_tree)
        
        # 加载更多按钮
        self.load_more_btn = QPushButton("加载更多")
        self.load_more_btn.setEnabled(False)
        self.load_more_btn.setToolTip("加载更多层级的元素")
        element_tree_layout.addWidget(self.load_more_btn)
        
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
        self.export_btn.clicked.connect(self.export_code)
        self.history_search_btn.clicked.connect(self.search_history)
        self.history_clear_btn.clicked.connect(self.clear_history)
        self.history_detail_btn.clicked.connect(self.view_history_detail)
        self.history_delete_btn.clicked.connect(self.delete_history_record)
        self.favorites_search_btn.clicked.connect(self.search_favorites)
        self.favorites_refresh_btn.clicked.connect(self.refresh_favorites_list)
        self.add_favorite_btn.clicked.connect(self.add_to_favorites)
        self.remove_favorite_btn.clicked.connect(self.remove_from_favorites)
        self.favorite_detail_btn.clicked.connect(self.view_favorite_detail)
        self.wizard_btn.clicked.connect(self.show_wizard)
        
        # 定位方式快捷按钮点击事件
        self.attr_btn.clicked.connect(lambda: self.on_locator_method_changed('attribute'))
        self.image_btn.clicked.connect(lambda: self.on_locator_method_changed('image'))
        self.coord_btn.clicked.connect(lambda: self.on_locator_method_changed('coordinate'))
        self.pyautogui_btn.clicked.connect(lambda: self.on_locator_method_changed('pyautogui'))
        self.win32gui_btn.clicked.connect(lambda: self.on_locator_method_changed('win32gui'))
        
        # 传统单选按钮点击事件
        self.attr_radio.toggled.connect(lambda checked: self.on_locator_radio_changed(checked, 'attribute'))
        self.image_radio.toggled.connect(lambda checked: self.on_locator_radio_changed(checked, 'image'))
        self.coord_radio.toggled.connect(lambda checked: self.on_locator_radio_changed(checked, 'coordinate'))
        
        # 元素树相关信号
        self.load_more_btn.clicked.connect(self.on_load_more_clicked)
        self.element_search_btn.clicked.connect(self.on_element_search)
        self.element_search_edit.returnPressed.connect(self.on_element_search)
    
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
        
        # 构建根元素
        root_element = self.element_analyzer.analyze_window(window)
        if root_element:
            # 创建根节点
            root_item = QTreeWidgetItem(self.element_tree)
            root_item.setText(0, f"{root_element.element_type} - {root_element.name or ''}")
            root_item.setData(0, Qt.UserRole, root_element)
            root_item.setData(0, Qt.UserRole + 1, False)  # 标记为未加载子节点
            
            # 添加一个占位节点，表示可以展开
            placeholder = QTreeWidgetItem(root_item)
            placeholder.setText(0, "Loading...")
            
            # 启用加载更多按钮
            self.load_more_btn.setEnabled(True)
            
            # 注册展开信号
            self.element_tree.itemExpanded.connect(self.on_item_expanded)
    
    def on_load_more_clicked(self):
        """处理加载更多按钮点击事件"""
        # 增加加载深度
        self.element_analyzer.initial_load_depth += 2
        self.update_status(f"加载深度已增加到: {self.element_analyzer.initial_load_depth}")
        
        # 重新加载元素树
        self.update_element_tree()
        
    def on_element_search(self):
        """处理元素树搜索事件"""
        keyword = self.element_search_edit.text().lower()
        
        if not keyword:
            # 如果搜索框为空，恢复所有节点
            self.restore_all_tree_items()
            return
        
        # 遍历所有节点，隐藏不匹配的节点
        self.filter_tree_items(self.element_tree.invisibleRootItem(), keyword)
    
    def filter_tree_items(self, parent_item, keyword):
        """过滤树节点
        
        Args:
            parent_item: 父节点
            keyword: 搜索关键字
        
        Returns:
            bool: 是否有匹配的子节点
        """
        has_matching_child = False
        
        for i in range(parent_item.childCount()):
            child_item = parent_item.child(i)
            element = child_item.data(0, Qt.UserRole)
            
            if element:
                # 检查元素是否匹配关键字
                match = keyword in element.element_type.lower() or (element.name and keyword in element.name.lower())
                
                # 递归过滤子节点
                child_has_match = self.filter_tree_items(child_item, keyword)
                
                # 如果当前节点匹配或有匹配的子节点，则显示
                if match or child_has_match:
                    child_item.setHidden(False)
                    # 展开有匹配子节点的父节点
                    if child_has_match:
                        child_item.setExpanded(True)
                    has_matching_child = True
                else:
                    child_item.setHidden(True)
            else:
                # 非元素节点（如Loading...）
                child_item.setHidden(True)
        
        return has_matching_child
    
    def restore_all_tree_items(self):
        """恢复所有树节点的显示"""
        def restore_items(parent_item):
            for i in range(parent_item.childCount()):
                child_item = parent_item.child(i)
                child_item.setHidden(False)
                child_item.setExpanded(False)
                restore_items(child_item)
        
        restore_items(self.element_tree.invisibleRootItem())
    
    def on_item_expanded(self, item):
        """处理树节点展开事件，异步加载子节点"""
        # 检查是否已加载子节点
        if item.childCount() == 1 and item.child(0).text(0) == "Loading...":
            # 删除占位节点
            item.takeChild(0)
            
            # 获取元素对象
            element = item.data(0, Qt.UserRole)
            
            # 异步加载子节点
            self.load_child_elements(element, item)
    
    def load_child_elements(self, parent_element, parent_item):
        """异步加载子元素，支持分层懒加载"""
        # 使用线程池异步加载子节点
        from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
        
        class LoadChildTask(QRunnable):
            """加载子元素的任务类"""
            def __init__(self, parent_element, parent_item, main_window):
                super().__init__()
                self.parent_element = parent_element
                self.parent_item = parent_item
                self.main_window = main_window
            
            @pyqtSlot()
            def run(self):
                """执行加载任务"""
                try:
                    # 检查是否已经加载过子元素
                    if self.parent_element.children:
                        # 已加载，直接使用
                        child_elements = self.parent_element.children
                    elif hasattr(self.parent_element, 'has_children') and self.parent_element.has_children:
                        # 需要动态加载子元素
                        from core.element_analyzer import ElementAnalyzer
                        import pywinauto
                        
                        # 重新连接应用并获取父元素
                        analyzer = ElementAnalyzer()
                        app = pywinauto.Application(backend='uia').connect(handle=self.parent_element.window_handle)
                        window = app.window(handle=self.parent_element.window_handle)
                        
                        # 构建定位条件
                        conditions = {}
                        if self.parent_element.automation_id:
                            conditions['auto_id'] = self.parent_element.automation_id
                        elif self.parent_element.name:
                            conditions['name'] = self.parent_element.name
                        elif self.parent_element.class_name:
                            conditions['class_name'] = self.parent_element.class_name
                        
                        # 查找父元素
                        if conditions:
                            found_element = window.child_window(**conditions)
                            if found_element.exists():
                                # 临时存储原始子元素列表
                                original_children = self.parent_element.children.copy()
                                
                                # 加载子元素
                                analyzer._analyze_element_children(found_element, self.parent_element, self.parent_element.depth + 1)
                                
                                # 计算新加载的子元素
                                new_children = [child for child in self.parent_element.children if child not in original_children]
                                child_elements = new_children
                            else:
                                child_elements = []
                        else:
                            child_elements = []
                    else:
                        child_elements = []
                except Exception as e:
                    print(f"动态加载子元素失败: {e}")
                    child_elements = []
                
                # 在主线程中更新UI
                from PyQt5.QtCore import QMetaObject, Q_ARG
                QMetaObject.invokeMethod(
                    self.main_window, "add_child_elements",
                    Q_ARG(object, child_elements),
                    Q_ARG(object, self.parent_item)
                )
        
        # 创建并启动任务
        task = LoadChildTask(parent_element, parent_item, self)
        QThreadPool.globalInstance().start(task)
    
    def add_child_elements(self, child_elements, parent_item):
        """将子元素添加到树节点"""
        for child in child_elements:
            # 创建子节点
            child_item = QTreeWidgetItem(parent_item)
            child_item.setText(0, f"{child.element_type} - {child.name or ''}")
            child_item.setData(0, Qt.UserRole, child)
            child_item.setData(0, Qt.UserRole + 1, False)  # 标记为未加载子节点
            
            # 检查是否有子元素或需要后续加载
            if child.children or (hasattr(child, 'has_children') and child.has_children):
                placeholder = QTreeWidgetItem(child_item)
                placeholder.setText(0, "Loading...")
    
    def on_element_selected(self, item, column):
        """元素树节点选中时的处理"""
        element = item.data(0, Qt.UserRole)
        if not element:
            return
        
        self.current_element = element
        
        # 计算元素稳定性评分和推荐定位策略
        self.element_analyzer.calculate_stability_score(element)
        
        # 更新元素详细信息
        self.update_element_info(element)
        
        # 更新定位路径
        self.update_element_path(element)
        
        # 生成定位代码
        self.generate_locator_code(element)
        
        # 显示定位策略建议
        self.show_locator_suggestions(element)
    
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
        
        # 添加稳定性评分和推荐定位策略
        if hasattr(element, 'stability_score') and element.stability_score is not None:
            properties.append(("定位稳定性评分", f"{element.stability_score}/100"))
        if hasattr(element, 'locator_strategy') and element.locator_strategy:
            properties.append(("推荐定位策略", element.locator_strategy))
        if hasattr(element, 'locator_priority') and element.locator_priority:
            properties.append(("定位方法优先级", ", ".join(element.locator_priority)))
        
        # 填充表格
        for row, (key, value) in enumerate(properties):
            self.element_info_table.insertRow(row)
            self.element_info_table.setItem(row, 0, QTableWidgetItem(key))
            self.element_info_table.setItem(row, 1, QTableWidgetItem(str(value)))
    
    def show_locator_suggestions(self, element):
        """显示定位策略建议"""
        if not hasattr(element, 'stability_suggestions') or not element.stability_suggestions:
            return
        
        # 显示定位策略建议
        suggestions = "\n".join([f"• {suggestion}" for suggestion in element.stability_suggestions])
        if suggestions:
            self.statusBar().showMessage(f"定位建议: {suggestions}")
    
    def update_element_path(self, element):
        """更新元素路径"""
        path = self.element_analyzer.get_element_path(element)
        self.path_text_edit.setPlainText(path)
    
    def generate_locator_code(self, element):
        """生成定位代码"""
        if not element:
            return
        
        # 确定当前选中的定位方法
        if self.attr_btn.isChecked():
            method = 'attribute'
        elif self.image_btn.isChecked():
            method = 'image'
        elif self.coord_btn.isChecked():
            method = 'coordinate'
        elif self.pyautogui_btn.isChecked():
            method = 'pyautogui'
        elif self.win32gui_btn.isChecked():
            method = 'win32gui'
        else:
            method = 'attribute'  # 默认使用属性定位
        
        # 生成pywinauto代码
        pywinauto_code = self.code_generator.generate_pywinauto_code(element)
        self.pywinauto_code_edit.setPlainText(pywinauto_code)
        
        # 生成uiautomation代码
        uiauto_code = self.code_generator.generate_uiautomation_code(element)
        self.uiauto_code_edit.setPlainText(uiauto_code)
    
    def on_locator_method_changed(self, method):
        """处理定位方式变化事件
        
        Args:
            method: 定位方法，可选值：attribute, image, coordinate, pyautogui, win32gui
        """
        # 更新快捷按钮状态
        self.attr_btn.setChecked(method == 'attribute')
        self.image_btn.setChecked(method == 'image')
        self.coord_btn.setChecked(method == 'coordinate')
        self.pyautogui_btn.setChecked(method == 'pyautogui')
        self.win32gui_btn.setChecked(method == 'win32gui')
        
        # 更新传统单选按钮状态
        if method == 'attribute':
            self.attr_radio.setChecked(True)
        elif method == 'image':
            self.image_radio.setChecked(True)
        elif method == 'coordinate':
            self.coord_radio.setChecked(True)
        
        # 更新当前选中的定位方法
        self.current_locator_method = method
        
        # 重新生成定位代码
        if self.current_element:
            self.generate_locator_code(self.current_element)
        
        self.update_status(f"已切换到{method}定位方式")
    
    def on_locator_radio_changed(self, checked, method):
        """处理传统单选按钮变化事件
        
        Args:
            checked: 是否选中
            method: 定位方法
        """
        if checked:
            # 同步到快捷按钮
            self.on_locator_method_changed(method)
    
    def start_capture(self):
        """开始捕获元素"""
        self.capture_btn.setText("捕获中...")
        self.capture_btn.setEnabled(False)
        self.update_status("正在捕获元素...")
        
        try:
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
                self.update_status(f"成功捕获元素: {element.element_type} - {element.name}")
            else:
                self.update_status("未捕获到元素")
        except Exception as e:
            self.show_error("捕获失败", f"捕获元素时发生错误: {str(e)}")
        finally:
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
            self.show_warning("警告", "请先选择或捕获一个元素")
            return
        
        # 确定当前选中的定位方法
        if hasattr(self, 'current_locator_method'):
            method = self.current_locator_method
        else:
            # 兼容旧的判断方式
            if self.attr_radio.isChecked():
                method = 'attribute'
            elif self.image_radio.isChecked():
                method = 'image'
            elif self.coord_radio.isChecked():
                method = 'coordinate'
            else:
                method = 'auto'
        
        try:
            self.update_status(f"正在测试{method}定位...")
            
            # 生成当前定位代码
            code = self.code_generator.generate_code_by_method(self.current_element, method)
            
            # 测试定位
            result = self.element_capture.test_element_location(self.current_element)
            
            # 可视化定位反馈
            if result:
                self._draw_element_border(self.current_element)
            
            # 保存历史记录
            self.history_manager.add_record(self.current_element, method, code, result)
            self.refresh_history_list()
            
            if result:
                self.show_info("成功", "定位成功！")
            else:
                self.show_warning("失败", "定位失败，请检查定位表达式")
        except Exception as e:
            self.show_error("测试定位失败", f"测试定位时发生错误: {str(e)}")
    
    def _draw_element_border(self, element):
        """在元素周围绘制动态边框
        
        Args:
            element: 要绘制边框的元素
        """
        try:
            import win32gui
            import win32con
            import win32api
            import time
            
            # 获取窗口句柄
            hwnd = win32gui.WindowFromPoint((element.x, element.y))
            if not hwnd:
                return
            
            # 绘制闪烁的红色矩形
            for i in range(3):  # 闪烁3次
                # 绘制红色矩形
                dc = win32gui.GetDC(hwnd)
                pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32gui.RGB(255, 0, 0))
                win32gui.SelectObject(dc, pen)
                win32gui.Rectangle(dc, element.x, element.y, element.x + element.width, element.y + element.height)
                win32gui.DeleteObject(pen)
                win32gui.ReleaseDC(hwnd, dc)
                
                # 短暂延迟
                time.sleep(0.3)
                
                # 清除矩形（重绘窗口）
                win32gui.RedrawWindow(hwnd, (element.x - 10, element.y - 10, element.x + element.width + 10, element.y + element.height + 10), None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
                
                # 短暂延迟
                time.sleep(0.3)
        except Exception as e:
            print(f"绘制元素边框失败: {e}")
    
    def refresh_history_list(self):
        """刷新历史记录列表"""
        records = self.history_manager.get_all_records()
        self.history_table.setRowCount(0)
        
        for record in records:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            # 格式化时间
            timestamp = record['timestamp'].split('.')[0] if '.' in record['timestamp'] else record['timestamp']
            
            self.history_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
            self.history_table.setItem(row, 1, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 2, QTableWidgetItem(record['application']))
            self.history_table.setItem(row, 3, QTableWidgetItem(record['element_type']))
            self.history_table.setItem(row, 4, QTableWidgetItem(record['method']))
    
    def search_history(self):
        """搜索历史记录"""
        keyword = self.history_search_edit.text()
        records = self.history_manager.search_records(keyword)
        self.history_table.setRowCount(0)
        
        for record in records:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            # 格式化时间
            timestamp = record['timestamp'].split('.')[0] if '.' in record['timestamp'] else record['timestamp']
            
            self.history_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
            self.history_table.setItem(row, 1, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 2, QTableWidgetItem(record['application']))
            self.history_table.setItem(row, 3, QTableWidgetItem(record['element_type']))
            self.history_table.setItem(row, 4, QTableWidgetItem(record['method']))
    
    def clear_history(self):
        """清空历史记录"""
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有历史记录吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_manager.clear_history()
            self.refresh_history_list()
            QMessageBox.information(self, "成功", "历史记录已清空")
    
    def view_history_detail(self):
        """查看历史记录详情"""
        current_row = self.history_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一条历史记录")
            return
        
        # 获取选中记录的ID
        record_id = int(self.history_table.item(current_row, 0).text())
        record = self.history_manager.get_record_by_id(record_id)
        
        if record:
            # 显示历史记录详情
            detail_dialog = QMessageBox()
            detail_dialog.setWindowTitle("历史记录详情")
            detail_dialog.setTextFormat(Qt.RichText)
            
            detail_text = f"<h3>历史记录详情</h3>"
            detail_text += f"<p><b>ID:</b> {record['id']}</p>"
            detail_text += f"<p><b>时间:</b> {record['timestamp']}</p>"
            detail_text += f"<p><b>应用:</b> {record['application']}</p>"
            detail_text += f"<p><b>元素类型:</b> {record['element_type']}</p>"
            detail_text += f"<p><b>元素名称:</b> {record['element_name']}</p>"
            detail_text += f"<p><b>Automation ID:</b> {record['automation_id']}</p>"
            detail_text += f"<p><b>类名:</b> {record['class_name']}</p>"
            detail_text += f"<p><b>定位方法:</b> {record['method']}</p>"
            detail_text += f"<p><b>定位结果:</b> {'成功' if record['result'] else '失败'}</p>"
            detail_text += f"<p><b>坐标:</b> ({record['coordinates']['x']}, {record['coordinates']['y']})</p>"
            detail_text += f"<p><b>尺寸:</b> {record['coordinates']['width']}x{record['coordinates']['height']}</p>"
            
            detail_dialog.setText(detail_text)
            detail_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Copy)
            
            if detail_dialog.exec_() == QMessageBox.Copy:
                # 复制代码到剪贴板
                from PyQt5.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(record['code'])
    
    def delete_history_record(self):
        """删除历史记录"""
        current_row = self.history_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一条历史记录")
            return
        
        # 获取选中记录的ID
        record_id = int(self.history_table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这条历史记录吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_manager.delete_record(record_id)
            self.refresh_history_list()
            QMessageBox.information(self, "成功", "历史记录已删除")
    
    def refresh_favorites_list(self):
        """刷新收藏夹列表"""
        favorites = self.favorites_manager.get_all_favorites()
        self.favorites_table.setRowCount(0)
        
        for fav in favorites:
            row = self.favorites_table.rowCount()
            self.favorites_table.insertRow(row)
            
            self.favorites_table.setItem(row, 0, QTableWidgetItem(str(fav['id'])))
            self.favorites_table.setItem(row, 1, QTableWidgetItem(fav['element_type']))
            self.favorites_table.setItem(row, 2, QTableWidgetItem(fav['element_name'] or ''))
            self.favorites_table.setItem(row, 3, QTableWidgetItem(', '.join(fav['tags'])))
    
    def search_favorites(self):
        """搜索收藏夹"""
        keyword = self.favorites_search_edit.text()
        favorites = self.favorites_manager.search_favorites(keyword)
        self.favorites_table.setRowCount(0)
        
        for fav in favorites:
            row = self.favorites_table.rowCount()
            self.favorites_table.insertRow(row)
            
            self.favorites_table.setItem(row, 0, QTableWidgetItem(str(fav['id'])))
            self.favorites_table.setItem(row, 1, QTableWidgetItem(fav['element_type']))
            self.favorites_table.setItem(row, 2, QTableWidgetItem(fav['element_name'] or ''))
            self.favorites_table.setItem(row, 3, QTableWidgetItem(', '.join(fav['tags'])))
    
    def add_to_favorites(self):
        """添加当前元素到收藏夹"""
        if not self.current_element:
            QMessageBox.warning(self, "警告", "请先选择或捕获一个元素")
            return
        
        # 添加到收藏夹
        success = self.favorites_manager.add_favorite(self.current_element)
        if success:
            self.refresh_favorites_list()
            QMessageBox.information(self, "成功", "元素已添加到收藏夹")
        else:
            QMessageBox.warning(self, "警告", "该元素已在收藏夹中")
    
    def remove_from_favorites(self):
        """从收藏夹移除元素"""
        current_row = self.favorites_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个收藏项")
            return
        
        # 获取选中收藏项的ID
        favorite_id = int(self.favorites_table.item(current_row, 0).text())
        
        reply = QMessageBox.question(
            self, "确认移除", "确定要从收藏夹移除这个元素吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.favorites_manager.remove_favorite(favorite_id)
            self.refresh_favorites_list()
            QMessageBox.information(self, "成功", "元素已从收藏夹移除")
    
    def view_favorite_detail(self):
        """查看收藏项详情"""
        current_row = self.favorites_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个收藏项")
            return
        
        # 获取选中收藏项的ID
        favorite_id = int(self.favorites_table.item(current_row, 0).text())
        favorite = self.favorites_manager.get_favorite_by_id(favorite_id)
        
        if favorite:
            # 显示收藏项详情
            detail_dialog = QMessageBox()
            detail_dialog.setWindowTitle("收藏项详情")
            detail_dialog.setTextFormat(Qt.RichText)
            
            detail_text = f"<h3>收藏项详情</h3>"
            detail_text += f"<p><b>ID:</b> {favorite['id']}</p>"
            detail_text += f"<p><b>添加时间:</b> {favorite['added_at']}</p>"
            detail_text += f"<p><b>应用:</b> {favorite['application']}</p>"
            detail_text += f"<p><b>元素类型:</b> {favorite['element_type']}</p>"
            detail_text += f"<p><b>元素名称:</b> {favorite['element_name']}</p>"
            detail_text += f"<p><b>Automation ID:</b> {favorite['automation_id']}</p>"
            detail_text += f"<p><b>类名:</b> {favorite['class_name']}</p>"
            detail_text += f"<p><b>标签:</b> {', '.join(favorite['tags'])}</p>"
            detail_text += f"<p><b>坐标:</b> ({favorite['coordinates']['x']}, {favorite['coordinates']['y']})</p>"
            detail_text += f"<p><b>尺寸:</b> {favorite['coordinates']['width']}x{favorite['coordinates']['height']}</p>"
            
            detail_dialog.setText(detail_text)
            detail_dialog.exec_()
    
    def create_wizard_dialog(self):
        """创建向导对话框"""
        self.wizard = QWizard()
        self.wizard.setWindowTitle("定位元素向导")
        self.wizard.setPage(1, self.create_wizard_page_1())
        self.wizard.setPage(2, self.create_wizard_page_2())
        self.wizard.setPage(3, self.create_wizard_page_3())
    
    def create_wizard_page_1(self):
        """创建向导第一页：选择应用"""
        page = QWizardPage()
        page.setTitle("第一步：选择应用")
        page.setSubTitle("请从列表中选择要定位的应用程序")
        
        layout = QVBoxLayout()
        label = QLabel("1. 选择一个正在运行的应用程序，然后点击'下一步'继续")
        layout.addWidget(label)
        layout.addWidget(QLabel("提示：如果列表中没有您需要的应用，请点击'刷新'按钮"))
        page.setLayout(layout)
        
        return page
    
    def create_wizard_page_2(self):
        """创建向导第二页：捕获元素"""
        page = QWizardPage()
        page.setTitle("第二步：捕获元素")
        page.setSubTitle("将鼠标移动到目标元素上，按下Ctrl键确认捕获")
        
        layout = QVBoxLayout()
        label = QLabel("2. 点击'开始捕获'按钮，然后将鼠标移动到目标元素上，按下Ctrl键确认")
        layout.addWidget(label)
        layout.addWidget(QLabel("提示：捕获成功后，元素信息将显示在右侧面板中"))
        page.setLayout(layout)
        
        return page
    
    def create_wizard_page_3(self):
        """创建向导第三页：生成代码"""
        page = QWizardPage()
        page.setTitle("第三步：生成代码")
        page.setSubTitle("查看并复制生成的定位代码")
        
        layout = QVBoxLayout()
        label = QLabel("3. 选择定位方法，查看生成的代码，然后点击'复制代码'或'导出代码'使用")
        layout.addWidget(label)
        layout.addWidget(QLabel("提示：您可以在'历史记录'和'收藏夹'标签中管理定位记录"))
        page.setLayout(layout)
        
        return page
    
    def show_wizard(self):
        """显示向导对话框"""
        self.wizard.show()
    
    def init_logging(self):
        """初始化日志记录"""
        import logging
        import os
        
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置日志
        logging.basicConfig(
            filename=os.path.join(log_dir, 'locator_desktop.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
        # 添加控制台日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
        
        logging.info("Locator_desktop 应用启动")
    
    def update_status(self, message):
        """更新状态栏消息
        
        Args:
            message: 要显示的消息
        """
        self.statusBar().showMessage(message)
        import logging
        logging.info(message)
    
    def show_error(self, title, message):
        """显示错误消息
        
        Args:
            title: 错误标题
            message: 错误消息
        """
        QMessageBox.critical(self, title, message)
        self.update_status(f"错误: {message}")
        import logging
        logging.error(f"{title}: {message}")
    
    def show_warning(self, title, message):
        """显示警告消息
        
        Args:
            title: 警告标题
            message: 警告消息
        """
        QMessageBox.warning(self, title, message)
        self.update_status(f"警告: {message}")
        import logging
        logging.warning(f"{title}: {message}")
    
    def show_info(self, title, message):
        """显示信息消息
        
        Args:
            title: 信息标题
            message: 信息消息
        """
        QMessageBox.information(self, title, message)
        self.update_status(message)
        import logging
        logging.info(f"{title}: {message}")
    
    def copy_code(self):
        """复制当前选中标签页的代码"""
        try:
            from PyQt5.QtWidgets import QApplication
            current_tab = self.code_tab.currentIndex()
            if current_tab == 0:
                code = self.pywinauto_code_edit.toPlainText()
            else:
                code = self.uiauto_code_edit.toPlainText()
            
            # 复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            self.show_info("成功", "代码已复制到剪贴板")
        except Exception as e:
            self.show_error("复制失败", f"复制代码时发生错误: {str(e)}")
    
    def export_code(self):
        """导出代码到文件"""
        if not self.current_element:
            self.show_warning("警告", "请先选择或捕获一个元素")
            return
        
        # 确定当前选中的定位方法
        if self.attr_radio.isChecked():
            method = 'attribute'
        elif self.image_radio.isChecked():
            method = 'image'
        elif self.coord_radio.isChecked():
            method = 'coordinate'
        else:
            method = 'auto'
        
        try:
            self.update_status("正在生成代码...")
            
            # 生成完整可执行脚本
            code = self.code_generator.generate_complete_script(self.current_element, method)
            
            # 弹出文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出代码", "generated_script.py", "Python Files (*.py);;All Files (*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(code)
                    self.show_info("成功", f"代码已导出到 {file_path}")
                    self.update_status(f"代码已导出到 {file_path}")
                except Exception as e:
                    self.show_error("导出失败", f"保存文件时发生错误: {str(e)}")
        except Exception as e:
            self.show_error("导出失败", f"生成代码时发生错误: {str(e)}")
    
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
