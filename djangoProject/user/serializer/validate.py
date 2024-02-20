#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：djangoProject 
@File    ：validate.py
@IDE     :PyCharm 
@Author  ：昊昊
@Date    ：2022-07-24  下午 2:36 
'''
import re
import json
# 验证手机号格式
import random
from django.conf import settings
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models

def MobileNumberVerification(value):
    """
    手机号验证
    :param Phone:
    :return:
    """
    if re.match('^(1[3|4|5|6|7|8|9])\d{9}$',str(value)):
        return True
    return False

# 随机生成验证码
def CreateCode():
    """
    生成随机验证码
    :return:Code:随机生成验证码
    """
    Code = random.randint(100000,999999)
    return str(Code)


# 发送短信验证码
def MobileCodeSend(TemplateId,Phone=None, Code=None):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(settings.TENCENT_SECRET_ID, settings.TENCENT_SECRET_KEY)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = sms_client.SmsClient(cred, settings.TENCENT_CITY, clientProfile)
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.SendSmsRequest()
        params = {
            "PhoneNumberSet": [Phone],
            "SmsSdkAppId": "1400711701",
            "SignName": "Django测试",
            "TemplateId": TemplateId,
            "TemplateParamSet": [Code]
        }
        req.from_json_string(json.dumps(params))
        # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
        resp = client.SendSms(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())
        return True
    except TencentCloudSDKException as err:
        print(err)
        return False