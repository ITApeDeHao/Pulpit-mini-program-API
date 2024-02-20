#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：djangoProject 
@File    ：account.py
@IDE     :PyCharm 
@Author  ：昊昊
@Date    ：2022-07-24  下午 2:30 
'''
from .validate import MobileNumberVerification
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection
from user import models
class MobileNumberserializer(serializers.Serializer):
    Phone = serializers.CharField(label="手机号",validators=[MobileNumberVerification,])

class Codeserializer(serializers.Serializer):
    Phone = serializers.CharField(label="手机号",validators=[MobileNumberVerification,])
    PassWord = serializers.CharField(label="密码", required=False)
    Code = serializers.CharField(label="验证码")
    resume = serializers.CharField(label='个人简介')

    def validate_PassWord(self, value):
        if not (6 <= len(value) <= 16):
            raise ValidationError("密码格式错误")
        return value

    def validate_Code(self, value):
        if len(value) != 6:
            raise ValidationError("验证码格式错误")
        Phone = self.initial_data.get('Phone')
        conn = get_redis_connection()
        Code = conn.get(Phone)
        if not Code:
            raise ValidationError("验证码过期")
        if value != Code.decode('utf-8'):
            raise ValidationError("验证码错误")
        return value

class PassWordserializer(serializers.Serializer):
    Phone = serializers.CharField(label="手机号", validators=[MobileNumberVerification,])
    PassWord = serializers.CharField(label="密码",allow_null=True)
    def validate_Phone(self, value):
        try:
            user = models.UserInfo.objects.get(Phone=value)
        except:
            raise ValidationError("用户不存在")
        return value

    def validate_PassWord(self, value):
        if not (6 <= len(value) <= 16):
            raise ValidationError("密码格式不正确")
        return value


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"