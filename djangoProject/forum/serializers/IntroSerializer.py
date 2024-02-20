# !/usr/bin/env python
# -*-coding:utf-8 -*-


# ProJect    : djangoProject
# File       : IntroSerializer.py
# Author     ：ITApeDeHao
# version    ：python 3.8
# Time       ：2023/3/7 21:46

"""
******************Description********************
"""
from rest_framework import serializers
from forum.models import ForumForummsg, ForumComment
from user.models import UserInfo

class IntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumForummsg
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumComment
        fields = "__all__"