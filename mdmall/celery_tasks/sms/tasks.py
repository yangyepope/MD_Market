# 编写异步任务代码

from celery_tasks.sms.aliyun_sms.aliyunSMS import AliyunSMS
from celery_tasks.main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信的celery异步任务
    :param mobile:  手机号
    :param sms_code:  验证码
    :return:
    """
    aliyun = AliyunSMS()
    aliyun.send_sms_request(mobile, sms_code)
