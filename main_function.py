# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_function.py
# Time       ：2023/3/30 23:55
# Author     ：wyatt
# Description：The main function py file for DA
"""

from main_ui import MainWindow, InputDialog, ScatterDialog, ArrayDialog
from PySide6.QtWidgets import QApplication, QFileDialog
import sys
from utils.regression import *
import numpy as np
import pandas as pd


# noinspection PyArgumentList
class MainFunction(MainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.Data = None
        self.X = None
        self.y = None
        self.title = None
        self.X_title = None
        self.y_title = None
        self.contain_title = None
        self.y_index = None
        self.ax = self.plot_canvas.axes
        self.file_open_button_action.triggered.connect(self.open_file)
        self.file_button.clicked.connect(self.check_file_button)
        self.data_button.clicked.connect(self.check_data_button)
        self.plot_button.clicked.connect(self.check_plot_button)
        self.exit_button_action.triggered.connect(self.clear_all)
        self.data_text_list.doubleClicked.connect(self.data_item_double_clicked)
        self.analysis_plot_scatter_button_action.triggered.connect(self.plot_scatter)

    def open_file(self):
        self.clear_all()
        self.file_path = QFileDialog.getOpenFileNames(self, '选择文件', './', '数据文件(*.csv *.xlsx)')[0][0]
        dialog = InputDialog()
        dialog.exec()
        self.contain_title = dialog.contain_title
        self.y_index = dialog.y_index
        self.file_text_list.addItem('Source: ' + self.file_path)
        self.file_text_list.addItem('--------------------------')
        if self.contain_title:
            if self.file_path.split('/')[-1].split('.')[-1] == 'csv':
                self.Data = pd.read_csv(self.file_path)
            else:
                self.Data = pd.read_excel(self.file_path)
            self.title = list(self.Data.columns)
            if self.y_index:
                self.y_title = self.title[self.y_index]
                _title = self.title.copy()
                _title.remove(self.y_title)
                self.X_title = _title
            else:
                self.X_title = self.title
        else:
            if self.file_path.split('/')[-1].split('.')[-1] == 'csv':
                self.Data = pd.read_csv(self.file_path, header=None)
            else:
                self.Data = pd.read_excel(self.file_path, header=None)
        if self.y_index is not None:
            self.y = np.array(self.Data.iloc[:, self.y_index]).flatten()
            if self.contain_title:
                self.X = np.array(
                    self.Data.loc[:, ~self.Data.columns.isin([str(self.Data.columns[self.y_index])])])
            else:
                self.X = np.array(
                    self.Data.loc[:, ~self.Data.columns.isin([int(self.Data.columns[self.y_index])])])
            self.data_text_list.addItem(f'Data{self.Data.shape[0]:->9}*{self.Data.shape[1]}')
            self.data_text_list.addItem(f'X{self.X.shape[0]:->12}*{self.X.shape[1]}')
            self.data_text_list.addItem(f'y{len(self.y):->12}')
        else:
            self.X = np.array(self.Data)
            self.data_text_list.addItem(f'Data{self.Data.shape[0]:->9}*{self.Data.shape[1]}')
            self.data_text_list.addItem(f'X{self.X.shape[0]:->12}*{self.X.shape[1]}')
        if self.y_title:
            self.data_text_list.addItem(f'X title{len(self.X_title):->4}')
            self.data_text_list.addItem(f'y title{len([self.y_title]):->4}')
        elif self.X_title:
            self.data_text_list.addItem(f'X title{len(self.X_title):->4}')
        self.Data = np.array(self.Data)
        self.y = self.y.reshape(-1, 1)
        self.X_title = np.array(self.X_title)
        self.y_title = np.array(self.y_title)
        self.X_title = self.X_title.reshape(1, -1)
        self.y_title = self.y_title.reshape(1, -1)

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

    def clear_all(self):
        self.file_path = None
        self.Data = None
        self.X = None
        self.y = None
        self.X_title = None
        self.y_title = None
        self.contain_title = None
        self.y_index = None
        self.ax.cla()
        self.plot_canvas.draw()
        self.data_text_list.clear()
        self.plot_text_list.clear()
        self.file_text_list.clear()
        self.file_text_list.addItem('请一次导入一个csv或xlsx文件')
        self.file_text_list.addItem('--------------------------')

    def data_item_double_clicked(self, item_index):
        item = self.data_text_list.item(item_index.row())
        array_name = item.text().split('-')[0].replace(' ', '_')
        array = getattr(self, array_name)
        dialog = ArrayDialog(array, array_name)
        dialog.setModal(False)
        dialog.show()
        dialog.exec()

    def plot_scatter(self):
        self.ax.cla()
        dialog = ScatterDialog()
        dialog.exec()
        x_variable_index = dialog.x_variable_index
        y_variable_index = dialog.y_variable_index
        linear_fit_switch = dialog.linear_fit_switch
        x = np.array(self.Data.iloc[:, x_variable_index]).flatten()
        y = np.array(self.Data.iloc[:, y_variable_index]).flatten()
        self.ax.scatter(x, y, marker='+', label='Original Data', alpha=0.8)
        if linear_fit_switch:
            w, b, r2, mse, mae, confidence = linear_fit(x, y)
            linear_x = np.linspace(np.min(x), np.max(x), 100)
            y_hat = w * linear_x + b
            self.ax.plot(linear_x, y_hat, 'r-', lw=2, label='Linear Fit Line')
            self.ax.plot(linear_x, y_hat - confidence, 'm:', lw=2, label='Confidence interval')
            self.ax.plot(linear_x, y_hat + confidence, 'm:', lw=2)
            if b >= 0:
                self.ax.set_title(
                    '$y = {:.5f}*x + {:.5f}$'.format(w, b) + '\n' + '$R^2 = {:.5f}$  MSE = {:.5f}  MAE = {:.5f}'.format(
                        r2, mse, mae),
                    fontdict={'fontsize': 13})
            else:
                self.ax.set_title(
                    '$y = {:.5f}*x {:.5f}$'.format(w, b) + '\n' + '$R^2 = {:.5f}$  MSE = {:.5f}  MAE = {:.5f}'.format(
                        r2, mse, mae),
                    fontdict={'fontsize': 13})
        if self.title:
            self.ax.set_xlabel(f'{self.title[x_variable_index]}', fontdict={'fontsize': 13})
            self.ax.set_ylabel(f'{self.title[y_variable_index]}', fontdict={'fontsize': 13})
        else:
            self.ax.set_xlabel('x variable', fontdict={'fontsize': 13})
            self.ax.set_ylabel('y variable', fontdict={'fontsize': 13})
        self.ax.legend(fontsize=12)
        self.ax.grid()
        self.plot_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainFunction()
    window.show()
    app.exec()
