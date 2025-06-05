import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django_redis import get_redis_connection


def send_password_change_code(email):
    conn = get_redis_connection('default')
    # 防止用户频繁发送验证码
    if conn.get(f'pwd_change_send:{email}'):
        raise ValueError('发送过于频繁，请稍后再试')

    # 生成验证码并缓存
    code = ''.join(random.choices(string.digits, k=4))
    conn.setex(f"pwd_change:{email}",300,code) #有效期5分钟
    conn.setex(f'pwd_change_send:{email}',60,1) # 发送验证码的间隔时间为60秒


    send_mail(
        '[ERP系统]密码修改验证码',
        f'您的验证码是：{code}，有效期为5分钟。',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
