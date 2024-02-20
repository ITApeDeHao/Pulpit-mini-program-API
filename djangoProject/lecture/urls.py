# !/usr/bin/env python
# -*-coding:utf-8 -*-


# ProJect    : djangoProject
# File       : urls.py
# Author     ：ITApeDeHao
# version    ：python 3.8
# Time       ：2023/3/11 22:44

"""
******************Description********************
"""
from django.urls import path
from lecture import views
urlpatterns = [
    path(r'',views.Lecture.as_view())
]