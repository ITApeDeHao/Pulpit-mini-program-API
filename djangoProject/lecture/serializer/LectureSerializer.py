# !/usr/bin/env python
# -*-coding:utf-8 -*-


# ProJect    : djangoProject
# File       : LectureSerializer.py.py
# Author     ：ITApeDeHao
# version    ：python 3.8
# Time       ：2023/3/11 22:47

"""
******************Description********************
"""
from rest_framework.serializers import ModelSerializer
from lecture.models import UniversityLecture
class LectureSerializer(ModelSerializer):
    class Meta:
        model = UniversityLecture
        fields = "__all__"