# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_ui.py
# Time       ：2023/3/30 10:28
# Author     ：wyatt
# Description：The main UI py file for DA
"""

from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QToolBar, \
    QMainWindow, QStatusBar
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('数据分析GUI')
        self.setMinimumSize(QSize(900, 600))

        self.toolbar = QToolBar('主工具栏')
        self.addToolBar(self.toolbar)

        self.file_button = QAction('文件', self)
        self.file_button.setStatusTip('文件操作')
        self.file_button.setCheckable(True)
        self.toolbar.addAction(self.file_button)

        self.toolbar.addSeparator()

        self.analyse_button = QAction('数据分析', self)
        self.analyse_button.setStatusTip('数据分析操作')
        self.analyse_button.setCheckable(True)
        self.toolbar.addAction(self.analyse_button)

        self.setStatusBar(QStatusBar(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
