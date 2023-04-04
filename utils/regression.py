# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : regression.py
# Time       ：2023/4/1 20:21
# Author     ：wyatt
# Description：Regression utils functions
"""
import numpy as np
import scipy.stats as ss


def linear_fit(x, y):
    x = np.array(x)
    y = np.array(y)
    linear_x = np.linspace(np.min(x), np.max(x), 100)
    n = len(x)
    w = (y * (x - x.mean())).sum() / ((x ** 2).sum() - x.sum() ** 2 / n)
    b = (y - w * x).sum() / n
    yhat = w * x + b
    tss = ((y - y.mean()) ** 2).sum()
    rss = ((y - yhat) ** 2).sum()
    r2 = 1 - rss / tss
    # k = 1  # 一元线性回归，自变量个数为1
    # r2_adj = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    mse = ((yhat - y) ** 2).sum() / n
    mae = np.abs(yhat - y).sum() / n
    alpha = 0.05
    tp = ss.t.isf(alpha / 2, df=n-2)
    sigma_hat = np.sqrt(rss / (n - 2))
    Lxx = ((x - x.mean()) ** 2).sum()
    confidence = tp * sigma_hat * np.sqrt(1 / n + (linear_x - linear_x.mean()) ** 2 / Lxx)
    return w, b, r2, mse, mae, confidence
