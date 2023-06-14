# -*- coding: utf-8 -*-
# @Time : 2023/6/14 11:23
# @Author : 祝佳祥
# @File : converters.py
# @Software: PyCharm
class UsernameConverter:
    """自定义路由转换器去匹配用户名"""
    # 定义匹配用户名的正则表达式
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        # 将匹配结果传递到视图内部时使用
        return str(value)

class UserMobileConverter:
    """自定义路由转换器去匹配用户名"""

    regex = '1[345789]\d{9}'

    def to_python(self, value):
        return str(value)