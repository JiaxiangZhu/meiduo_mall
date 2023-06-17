# -*- coding: utf-8 -*-
# @Time : 2023/6/17 15:49
# @Author : 祝佳祥
# @File : tasks.py
# @Software: PyCharm

from django.core.mail import send_mail
from Celery_task.celery_main import celery_app


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_url):
    subject = '美多商城激活邮件'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    message = ''
    from_email = '美多商城<zsjsxg@163.com>'

    send_mail(subject, message, from_email, [to_email], html_message=html_message)
