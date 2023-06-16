# -*- coding: utf-8 -*-
# @Time : 2023/6/15 17:06
# @Author : 祝佳祥
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<usermobile:mobile>/', SmsCodeView.as_view()),
]