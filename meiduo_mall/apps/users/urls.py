# -*- coding: utf-8 -*-
# @Time : 2023/6/13 12:03
# @Author : 祝佳祥
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from apps.users.views import UsernameCountView, UserMobileCountView, RegisterView, LoginView, LogoutView
from apps.users.views import CenterView, EmailView

urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 判断手机号是否重复
    path('mobiles/<usermobile:mobile>/count/', UserMobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    ]

