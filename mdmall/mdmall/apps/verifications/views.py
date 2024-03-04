from random import random, randint

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from mdmall.libs.aliyunSMS import AliyunSMS
import logging


# Create your views here.

class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1. 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        # 2. 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 3. 把验证码存储到redis数据库
        redis_conn.setex('sms_%s' % mobile, 600, sms_code, )
        # 4. 利用阿里云发送短信验证码
        aliyun = AliyunSMS()
        aliyun.send_sms_request(mobile, sms_code)
        # 5. 响应
        return Response({'code': 'OK'})
