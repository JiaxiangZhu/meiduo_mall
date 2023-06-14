"""
URL configuration for meiduo_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from utils.converters import UsernameConverter, UserMobileConverter
from django.urls import register_converter

# def log(request):
#     # 1. 导入
#     import logging
#     # 2. 创建日志器
#     logger = logging.getLogger('django')
#     # 3. 调动日志器的方法来保存日志
#     logger.info('用户登陆了')
#     logger.warning('redis缓存不足')
#     logger.error('该记录不存在')
#     logger.debug('~~~~~~~~~~~~~~~~~~')
#
#     return HttpResponse('log')

# 注册转换器
register_converter(UsernameConverter, 'username')
register_converter(UserMobileConverter, 'usermobile')

urlpatterns = [
    path('admin/', admin.site.urls),
    # 导入users子应用的路由
    path('', include('apps.users.urls'))
]
