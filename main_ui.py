# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_ui.py
# Time       ：2023/3/30 10:28
# Author     ：wyatt
# Description：The main UI py file for DA
"""

from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QToolBar, \
    QMainWindow, QStatusBar, QLabel, QListWidget, QStackedLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('数据分析GUI')
        self.setMinimumSize(QSize(900, 600))

        self.toolbar = QToolBar('主工具栏')
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        self.exit_button_action = QAction(QIcon('./icons/exit.png'), '关闭', self)
        self.exit_button_action.setStatusTip('关闭当前图层的图像')
        self.toolbar.addAction(self.exit_button_action)

        self.toolbar.addSeparator()

        self.zoom_in_button_action = QAction(QIcon('./icons/zoom_in.png'), '放大', self)
        self.zoom_in_button_action.setStatusTip('放大当前图层的图像')
        self.toolbar.addAction(self.zoom_in_button_action)

        self.toolbar.addSeparator()

        self.zoom_out_button_action = QAction(QIcon('./icons/zoom_out.png'), '缩小', self)
        self.zoom_out_button_action.setStatusTip('缩小当前图层的图像')
        self.toolbar.addAction(self.zoom_out_button_action)

        self.setStatusBar(QStatusBar(self))

        self.menu = self.menuBar()

        self.file_open_button_action = QAction('导入', self)
        self.file_open_button_action.setStatusTip('导入一个待分析数据文件')
        self.analysis_plot_scatter_button_action = QAction('散点图')
        self.analysis_plot_box_button_action = QAction('箱线图')
        self.analysis_outlier_button_action = QAction('离群点分析')
        self.analysis_regression_button_action = QAction('回归分析')
        self.analysis_classification_button_action = QAction('分类分析')
        self.analysis_clustering_button_action = QAction('聚类分析')
        self.analysis_reduction_button_action = QAction('降维分析')

        self.file_menu = self.menu.addMenu('文件')
        self.file_menu.addAction(self.file_open_button_action)
        self.analysis_menu = self.menu.addMenu('分析')
        self.analysis_plot_submenu = self.analysis_menu.addMenu('画图')
        self.analysis_plot_submenu.addAction(self.analysis_plot_scatter_button_action)
        self.analysis_plot_submenu.addAction(self.analysis_plot_box_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_outlier_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_regression_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_classification_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_clustering_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_reduction_button_action)

        self.file_button = QPushButton('显示文件')
        self.data_button = QPushButton('显示数据')
        self.plot_button = QPushButton('显示图像')
        self.file_button.setCheckable(True)
        self.data_button.setCheckable(True)
        self.plot_button.setCheckable(True)

        self.file_text_list = QListWidget()
        self.data_text_list = QListWidget()
        self.plot_list = QListWidget()
        self.plot_label = QLabel()

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.file_button)
        self.button_layout.addWidget(self.data_button)
        self.button_layout.addWidget(self.plot_button)

        self.info_layout = QStackedLayout()
        self.info_layout.addWidget(self.file_text_list)
        self.info_layout.addWidget(self.data_text_list)
        self.info_layout.addWidget(self.plot_list)
        self.info_layout.setCurrentIndex(0)

        self.layout1 = QVBoxLayout()
        self.layout1.addLayout(self.button_layout)
        self.layout1.addLayout(self.info_layout)

        self.plot_layout = QHBoxLayout()
        self.plot_layout.addWidget(self.plot_label)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.setStretch(0, 2)
        self.main_layout.setStretch(1, 10)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
