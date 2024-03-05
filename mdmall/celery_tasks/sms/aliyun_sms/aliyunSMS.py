"""
签名名称:阿里云短信测试
使用场景：发送测试短信
模版名称：测试专用模板
模版Code：SMS_154950909
模版类型：验证码
模版内容：您正在使用阿里云短信测试服务，体验验证码是：${code}，如非本人操作，请忽略本短信！

"""

from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions
import json


class AliyunSMS:
    access_key_id = 'LTAI5tDbUhg3xGGAKytqXJuf'
    access_key_secret = 'Sx3rpALoGP8tXRgbzxBUtQoCUVd8Ge'
    endpoint = 'dysmsapi.aliyuncs.com'
    sign_name = '阿里云短信测试'
    template_code = 'SMS_154950909'

    def __init__(self):
        self.config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=self.endpoint
        )

    def send_sms_request(self, mobile: str, code: str):
        """

        :param mobile: 手机号
        :param code: 短信验证码
        :return:
        """
        # 1. 创建客户端连接对象
        client = Client(self.config)
        send_sms_request = SendSmsRequest(
            phone_numbers=mobile,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=json.dumps({"code": code})
        )

        # 2. 设置运行超时时间
        runtime = RuntimeOptions()

        # 3. 发送短信
        try:
            res = client.send_sms_with_options(send_sms_request, runtime=runtime)
            # print(res)
            if res.body.code == 'OK':
                return {'code': 'OK', 'message': '短信发送成功'}
            else:
                return {'code': 'NO', 'error': res.body.message}

        except Exception as e:
            # 错误 message
            return {"code": "NO", "error": "短信发送失败"}


if __name__ == '__main__':
    aliyun = AliyunSMS()
    request = aliyun.send_sms_request(mobile='13076908699', code='1234')
    print(request)
