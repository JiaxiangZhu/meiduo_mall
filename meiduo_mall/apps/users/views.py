import json
import re

from MySQLdb import DatabaseError
from django.contrib.auth import logout
from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
"""
需求分析： 根据页面的功能（从上到下，从左到右），哪些功能需要和后端配合完成
如何确定哪些功能需要和后端进行交互呢？
        1.经验
        2.关注类似网址的相似功能
"""

"""
判断用户名是否重复的功能。
前端：
    当用户输入用户名之后，失去焦点，发送一个axios（ajax）请求
后端（思路）：
    请求：         接收用户名
    业务逻辑：      根据用户名查询数据库，如果查询结果数量等于0，说明没有注册
                    如果查询结果数量等与1，说明有注册
    响应：         JSON
                    {code:0,count:0/1,errmsg:ok}
    路由          GET     	usernames/<username>/count/
    （步骤）：
            1.  接收用户名
            2.  根据用户名查询数据库
            3.  返回响应
"""
# 由于一个视图需要处理不同的请求，如GET/POST等请求，所以使用类视图
from django.views import View
from apps.users.models import User
from django.http import JsonResponse


class UsernameCountView(View):

    def get(self, request, username):
        # 1.  接收用户名，对用户名进行一下判断

        # 2.  根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3.  返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

class UserMobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

"""
后端不信任前端提交的任何数据！！！！！
前端：     当用户输入用户名、密码、确认密码、手机号，是否同意协议之后，会点击注册按钮
            前端会发送axios请求
后端：
    请求：         接收请求（JSON)，获取数据
    业务逻辑：       验证数据，数据入库
    响应：         JSON{'code':0, 'errmsg': 'ok'}
                    响应码 0 表示成功 400表示失败
    路由：     POST    register/
步骤：
    1. 接受请求（POST--------JSON）
    2. 获取数据
    3. 验证数据
        3.1 用户名、密码、确认密码、手机号，是否同意协议 都要有
        3.2 用户名满足规则且不能重复
        3.3 密码满足规则
        3.4 确认密码和密码一致
        3.5 手机号满足规则，手机号也不能重复
        3.6 需要同意协议
    4. 数据入库
    5. 返回响应
"""

class RegisterView(View):

    def post(self, request):
        # 1. 接受请求（POST--------JSON）
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        # 3. 验证数据
        #     3.1 用户名、密码、确认密码、手机号，是否同意协议 都要有
        # all 中的元素，只要是Flase或None，就返回False，否则返回True
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用不明不满足规则'})
        #     3.2 用户名满足规则且不能重复
        #     3.3 密码满足规则
        #     3.4 确认密码和密码一致
        #     3.5 手机号满足规则，手机号也不能重复
        #     3.6 需要同意协议
        #   短信验证码测试
        redis_conn = get_redis_connection('code')
        sms_data = redis_conn.get(f'{mobile}')
        if not sms_data:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        if sms_code != sms_data.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码错误'})

        # 4. 数据入库
        # user = User(username=username, password=password, mobile=mobile)
        # user.save()
        # User.objects.create(username=username, password=password, mobile=mobile)
        # 以上两种方式都可以数据入库，但是存在一个问题，密码没有加密
        # 密码加密
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})

        # 如何设置session信息
        # request.session['user_id']=user.id
        # 系统（Django）为我们提供了状态保持的方法
        from django.contrib.auth import login
        # request, user,
        # 状态保持 -- 登录用户的状态保持
        login(request, user)
        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持（注册成功即已经登录）
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持（注册成功，单独登录）

实现状态保持主要有两种方式：
    在客户端存储信息使用Cookie
    在服务器端存储信息使用Session
"""

# 用户登录
class LoginView(View):

    def post(self, request):
        # 1. 接受请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2. 获取参数
        username = body_dict.get('username')
        password = body_dict.get('password')
        remembered = body_dict.get('remembered')

        if not all([username, password, remembered]):
            return JsonResponse({'code': 400, 'errmsg': '未填写账号密码'})

        # 需要确定是根据手机号查询还是根据用户名查询
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.object.get(username=username)

        # 方式2
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回User信息
        # 如果用户名和密码不正确，则返回None
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 4. session
        from django.contrib.auth import login
        login(request, user)

        # 5. 判断是否记住登录
        if not remembered:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600*24*15)
        return response

class LogoutView(View):

    def delete(self, request):
        # 清理session
        logout(request)
        # 退出登录，重定向到首页
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 退出登录时，清除cookie中的username
        response.delete_cookie('username')

        return response
from utils.views import LoginRequiredJSONMixin
class CenterView(LoginRequiredJSONMixin, View):

    def get(self, request):
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
