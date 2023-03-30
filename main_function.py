# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_function.py
# Time       ：2023/3/30 23:55
# Author     ：wyatt
# Description：The main function py file for DA
"""

from main_ui import MainWindow
from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QToolBar, \
    QMainWindow, QStatusBar, QLabel, QListWidget
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
import sys


class MainFunction(MainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.file_open_button_action.triggered.connect(self.open_file)
        self.data_button.clicked.connect(self.check_plot_button)
        self.plot_button.clicked.connect(self.check_data_button)

    def open_file(self):
        self.file_path = QFileDialog.getOpenFileNames(self, '选择文件', './')[0][0]
        self.text_list.addItem(self.file_path)

    def check_data_button(self):
        plot_button_check = self.plot_button.isChecked()
        if plot_button_check:
            self.data_button.setChecked(False)
            self.info_layout.setCurrentIndex(1)

    def check_plot_button(self):
        file_button_check = self.data_button.isChecked()
        if file_button_check:
            self.plot_button.setChecked(False)
            self.info_layout.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainFunction()
    window.show()
    app.exec()
