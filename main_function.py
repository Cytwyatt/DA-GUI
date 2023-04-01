# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_function.py
# Time       ：2023/3/30 23:55
# Author     ：wyatt
# Description：The main function py file for DA
"""

from main_ui import MainWindow, InputDialog, MplCanvas
from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QToolBar, \
    QMainWindow, QStatusBar, QLabel, QListWidget, QDialog, QDialogButtonBox, QRadioButton, QLineEdit
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
import sys
import numpy as np
import pandas as pd


# noinspection PyArgumentList
class MainFunction(MainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.data = None
        self.X = None
        self.y = None
        self.X_title = None
        self.y_title = None
        self.contain_title = None
        self.y_index = None
        self.ax = None
        self.file_open_button_action.triggered.connect(self.open_file)
        self.file_button.clicked.connect(self.check_file_button)
        self.data_button.clicked.connect(self.check_data_button)
        self.plot_button.clicked.connect(self.check_plot_button)
        self.analysis_plot_scatter_button_action.triggered.connect(self.plot_scatter)

    def open_file(self):
        self.file_text_list.clear()
        self.data_text_list.clear()
        self.plot_text_list.clear()
        self.file_text_list.addItem('请一次导入一个csv或xlsx文件')
        self.file_text_list.addItem('--------------------------')
        self.file_path = QFileDialog.getOpenFileNames(self, '选择文件', './', '数据文件(*.csv *.xlsx)')[0][0]
        dialog = InputDialog()
        dialog.exec()
        self.contain_title = dialog.contain_title
        self.y_index = dialog.y_index
        self.file_text_list.addItem('Source: ' + self.file_path)
        self.file_text_list.addItem('--------------------------')
        if self.contain_title:
            if self.file_path.split('/')[-1].split('.')[-1] == 'csv':
                self.data = pd.read_csv(self.file_path)
            else:
                self.data = pd.read_excel(self.file_path)
            title = list(self.data.columns)
            if self.y_index:
                self.y_title = title[self.y_index]
                title.remove(self.y_title)
                self.X_title = title
            else:
                self.X_title = title
        else:
            if self.file_path.split('/')[-1].split('.')[-1] == 'csv':
                self.data = pd.read_csv(self.file_path, header=None)
            else:
                self.data = pd.read_excel(self.file_path, header=None)
        if self.y_index is not None:
            self.y = np.array(self.data.iloc[:, self.y_index]).flatten()
            if self.contain_title:
                self.X = np.array(
                    self.data.loc[:, ~self.data.columns.isin([str(self.data.columns[self.y_index])])])
            else:
                self.X = np.array(
                    self.data.loc[:, ~self.data.columns.isin([int(self.data.columns[self.y_index])])])
            self.data_text_list.addItem(f'Data{self.data.shape[0]:->9}*{self.data.shape[1]}')
            self.data_text_list.addItem(f'X{self.X.shape[0]:->12}*{self.X.shape[1]}')
            self.data_text_list.addItem(f'y{len(self.y):->12}')
        else:
            self.X = np.array(self.data)
            self.data_text_list.addItem(f'Data{self.data.shape[0]:->9}*{self.data.shape[1]}')
            self.data_text_list.addItem(f'X{self.X.shape[0]:->12}*{self.X.shape[1]}')
        if self.y_title:
            self.data_text_list.addItem(f'X Title{len(self.X_title):->4}')
            self.data_text_list.addItem(f'y Title{len([self.y_title]):->4}')
        elif self.X_title:
            self.data_text_list.addItem(f'X Title{len(self.X_title):->4}')

    def check_plot_button(self):
        plot_button_check = self.plot_button.isChecked()
        if plot_button_check:
            self.file_button.setChecked(False)
            self.data_button.setChecked(False)
            self.info_layout.setCurrentIndex(2)

    def check_data_button(self):
        data_button_check = self.data_button.isChecked()
        if data_button_check:
            self.file_button.setChecked(False)
            self.plot_button.setChecked(False)
            self.info_layout.setCurrentIndex(1)

    def check_file_button(self):
        file_button_check = self.file_button.isChecked()
        if file_button_check:
            self.data_button.setChecked(False)
            self.plot_button.setChecked(False)
            self.info_layout.setCurrentIndex(0)

    def plot_scatter(self):
        self.ax = self.plot_canvas.axes
        self.ax.cla()
        self.ax.scatter(self.X, self.y)
        self.plot_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainFunction()
    window.show()
    app.exec()
