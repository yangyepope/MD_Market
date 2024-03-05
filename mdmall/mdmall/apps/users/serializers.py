import re

from django_redis import get_redis_connection
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""

    # 需要序列化的字段: ['id','username','mobile']
    # 需要反序列化的字段: ['username','password','password2','mobile','sms_code','allow']
    password2 = serializers.CharField(label='确认密码', write_only=True)  # write_only表示只做反序列化
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)  # 'true'

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错的错误提示
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, mobile):
        """单独校验手机号"""
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式有误')
        return mobile

    def validate_allow(self, allow):
        """是否同意协议校验"""

        if allow == 'true':
            raise serializers.ValidationError('请同意用户协议')
        return allow

    def validate(self, attrs):
        """校验密码是否相同"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 验证验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)

        # 向redis存储数据时都是以字符串进行存储的,取出来后都是bytes类型 [bytes]

        if real_sms_code is not None or attrs['sms_code'] != real_sms_code:
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(validated_data[password])
        user.save()

        return user
