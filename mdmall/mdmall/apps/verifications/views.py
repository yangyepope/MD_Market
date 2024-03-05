from random import random, randint

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from mdmall.apps.verifications import constans
from mdmall.libs.aliyunSMS import AliyunSMS
import logging

logger = logging.getLogger('django')


# Create your views here.

class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1. 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 2. 先从redis获取发送标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)

        # 3. 校验标记
        if send_flag:
            return Response({'message': "手机频繁发送短信"}, status=status.HTTP_400_BAD_REQUEST)
        # 4. 生成验证码
        sms_code = '%06d' % randint(0, 999999)
        logger.info(sms_code)

        # 优化redis性能,通过创建redis管道(把多次redis的操作装入管道，将来一次性去执行,减少redis连接操作)
        pl = redis_conn.pipeline()
        # 5. 把验证码存储到redis数据库
        pl.setex('sms_%s' % mobile, constans.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 6 存储一个标记，表示此手机号已经发送过短信 标记有效期60S
        pl.setex('send_flag_%s' % mobile, constans.SEND_SMS_CODE_INTERVAL, 1)

        # 执行redis管道
        pl.execute()

        # 7. 利用阿里云发送短信验证码
        aliyun = AliyunSMS()
        aliyun.send_sms_request(mobile, sms_code)

        # 8. 响应
        return Response({'code': 'OK'})
