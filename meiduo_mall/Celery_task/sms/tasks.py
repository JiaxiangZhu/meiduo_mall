# -*- coding: utf-8 -*-
# @Time : 2023/6/16 15:30
# @Author : 祝佳祥
# @File : tasks.py
# @Software: PyCharm

from libs.yuntongxun import sms_sendmessage
from Celery_task.celery_main import celery_app

# name:异步任务别名
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, data_code):
    sms_sendmessage.send_message(mobile, data_code)
