# -*- coding: utf-8 -*-
# @Time : 2023/6/13 12:03
# @Author : 祝佳祥
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from apps.users.views import UsernameCountView, UserMobileCountView, RegisterView

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 判断手机号是否重复
    path('mobiles/<usermobile:mobile>/count/', UserMobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    ]

