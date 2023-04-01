# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_ui.py
# Time       ：2023/3/30 10:28
# Author     ：wyatt
# Description：The main UI py file for DA
"""

from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QToolBar, \
    QMainWindow, QStatusBar, QLabel, QListWidget, QStackedLayout, QRadioButton, QLineEdit, QDialog, QDialogButtonBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon, QFont
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import pandas as pd


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        welcome_data = np.array(pd.read_csv('./welcome.csv', header=None))
        self.axes.plot(welcome_data[:, 0], welcome_data[:, 1])
        super(MplCanvas, self).__init__(self.fig)


# noinspection PyUnresolvedReferences
class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.y_index = None
        self.contain_title = None
        self.setWindowTitle('输入文件设置')

        self.title_label = QLabel('是否包含标题行')
        self.y_index_label = QLabel('标签值所在列,0表示第一列,-1表示最后一列,不输入表示没有标签')

        self.is_contain_title = QRadioButton('包含')
        self.not_contain_title = QRadioButton('不包含')
        self.is_contain_title.toggled.connect(self.contain_or_not)
        self.not_contain_title.toggled.connect(self.contain_or_not)

        self.y_index_edit = QLineEdit()

        self.button = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(self.button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.title_button_layout = QHBoxLayout()
        self.title_button_layout.addWidget(self.is_contain_title)
        self.title_button_layout.addWidget(self.not_contain_title)

        self.title_layout = QVBoxLayout()
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addLayout(self.title_button_layout)
        self.title_layout.addWidget(self.y_index_label)
        self.title_layout.addWidget(self.y_index_edit)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.title_layout)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def contain_or_not(self):
        if self.is_contain_title.isChecked():
            self.contain_title = True
        else:
            self.contain_title = False

    def accept(self):
        super().accept()
        if self.y_index_edit.text():
            self.y_index = int(self.y_index_edit.text())


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
        self.preprocess_outlier_button_action = QAction('离群点分析')
        self.analysis_plot_scatter_button_action = QAction('散点图')
        self.analysis_plot_box_button_action = QAction('箱线图')
        self.analysis_plot_hist_button_action = QAction('直方图')
        self.analysis_regression_button_action = QAction('回归分析')
        self.analysis_classification_button_action = QAction('分类分析')
        self.analysis_clustering_button_action = QAction('聚类分析')
        self.analysis_reduction_button_action = QAction('降维分析')
        self.postprocess_pdp_button_action = QAction('PDP分析')
        self.postprocess_ale_button_action = QAction('ALE分析')
        self.postprocess_shap_button_action = QAction('Shap分析')

        self.file_menu = self.menu.addMenu('文件')
        self.file_menu.addAction(self.file_open_button_action)
        self.preprocess_menu = self.menu.addMenu('预处理')
        self.preprocess_menu.addAction(self.preprocess_outlier_button_action)
        self.analysis_menu = self.menu.addMenu('分析')
        self.analysis_plot_submenu = self.analysis_menu.addMenu('画图')
        self.analysis_plot_submenu.addAction(self.analysis_plot_scatter_button_action)
        self.analysis_plot_submenu.addAction(self.analysis_plot_box_button_action)
        self.analysis_plot_submenu.addAction(self.analysis_plot_hist_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_regression_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_classification_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_clustering_button_action)
        self.analysis_menu.addSeparator()
        self.analysis_menu.addAction(self.analysis_reduction_button_action)
        self.postprocess_menu = self.menu.addMenu('后处理')
        self.postprocess_interpretation_submenu = self.postprocess_menu.addMenu('可解释性分析')
        self.postprocess_interpretation_submenu.addAction(self.postprocess_pdp_button_action)
        self.postprocess_interpretation_submenu.addAction(self.postprocess_ale_button_action)
        self.postprocess_interpretation_submenu.addAction(self.postprocess_shap_button_action)

        self.file_button = QPushButton('显示文件')
        self.data_button = QPushButton('显示数据')
        self.plot_button = QPushButton('显示图像')
        self.file_button.setCheckable(True)
        self.data_button.setCheckable(True)
        self.plot_button.setCheckable(True)

        self.file_text_list = QListWidget()
        self.file_text_list.addItem('请一次导入一个csv或xlsx文件')
        self.file_text_list.addItem('--------------------------')
        self.data_text_list = QListWidget()
        self.plot_text_list = QListWidget()
        self.plot_canvas = MplCanvas(self)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)
        self.file_text_list.setFont(QFont('Times', 12))
        self.data_text_list.setFont(QFont('Times', 12))
        self.plot_text_list.setFont(QFont('Times', 12))

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.file_button)
        self.button_layout.addWidget(self.data_button)
        self.button_layout.addWidget(self.plot_button)

        self.info_layout = QStackedLayout()
        self.info_layout.addWidget(self.file_text_list)
        self.info_layout.addWidget(self.data_text_list)
        self.info_layout.addWidget(self.plot_text_list)
        self.info_layout.setCurrentIndex(0)

        self.layout1 = QVBoxLayout()
        self.layout1.addLayout(self.button_layout)
        self.layout1.addLayout(self.info_layout)

        self.plot_layout = QVBoxLayout()
        self.plot_layout.addWidget(self.plot_toolbar)
        self.plot_layout.addWidget(self.plot_canvas)

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
