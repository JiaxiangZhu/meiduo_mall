# -*- coding: utf-8 -*-
# @Time : 2023/6/16 15:24
# @Author : 祝佳祥
# @File : celery_main.py
# @Software: PyCharm

from celery import Celery

#为使用celery使用django配置文件进行设置
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')

# 创建celery实例
celery_app = Celery('celery_tasks')
# 加载celery配置
celery_app.config_from_object('Celery_task.config')
# 自动注册celery任务
celery_app.autodiscover_tasks(['Celery_task.sms'])

# 启动
# celery -A celery_tasks.main worker -l info -P eventlet
