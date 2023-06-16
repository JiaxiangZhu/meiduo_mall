from random import randint

from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection

from Celery_task.sms.tasks import send_sms_code

"""
前端：
    拼接一个 URL ，然后给img， img会发送请求
    url=http://ip:port/image_codes/uuid/
后端：
    请求：     接收路由中的uuid
    业务逻辑：   生成图片验证码和图片二进制，通过redis吧图片验证码保存起来
    响应：     返回图片二进制
    路由：     GET     image_codes/uuid/
    
    步骤：
        1.获取uuid
        2.生成图片和验证码
        3.用redis保存验证码
        4.返回前端图片二进制
"""

# Create your views here.
class ImageCodeView(View):

    def get(self, request, uuid):
        # 1.获取uuid
        # 2.生成图片和验证码
        from libs.captcha.captcha import captcha
        # text 是图片验证码的内容，例如：XYZZ
        # image 是图片二进制
        text, image = captcha.generate_captcha()
        # 3.用redis保存验证码
        # 3.1 进行redis链接
        redis_cli = get_redis_connection('code')
        # 3.2 指令操作
        redis_cli.setex(uuid, 100, text)
        # 4.返回前端图片二进制
        # 因为图片是二进制，不能返回JSON数据
        # content_type 响应体数据类型
        # content_type 语法形式： 大类/小类
        return HttpResponse(image, content_type='image/jpeg')


"""
前端：
        当用户输入完手机号，图片验证码之后，前端发送一个axios请求
后端：
    请求：     接收请求，获取请求参数（路由有手机号，用户的图片验证码和UUID在查询字符串中）
    业务逻辑：   验证参数，验证图片验证码，生成短信验证码，保存短信验证码，发送短信验证码
    响应：     返回响应
                {'code':0, 'errmsg':'ok'}
    路由：http://www.meiduo.site:8000/sms_codes/13180837902/?image_code=H8AF&image_code_id=f7e302a1-da81-4ccb-9a82-2d8be32227a2        
    步骤：
        1.获取请求参数
        2.验证参数
        3.验证图片验证码
        4.生成短信验证码
        5.保存短信验证码
        6.发送短信验证码
        7.返回响应
"""

class SmsCodeView(View):

    def get(self, request, mobile):
        # 1.获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3.验证图片验证码
        redis_conn = get_redis_connection('code')
        redis_image_code = redis_conn.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 避免频繁发送短信验证码
        send_flag = redis_conn.get(f'send_flag_{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁，请稍后再试'})
        # 4.生成短信验证码
        data_code = '%04d' % randint(0, 9999)
        # 5.保存短信验证码
        # 创建redis pipeline
        redis_pl = redis_conn.pipeline()
        # 将redis请求添加到队列
        redis_pl.setex(mobile, 180, data_code)
        redis_pl.setex(f'send_flag_{mobile}', 60, 1)
        # 执行请求
        redis_pl.execute()
        # 6.发送短信验证码
        # from libs.yuntongxun import sms_sendmessage
        # sms_sendmessage.send_message(mobile, data_code)
        send_sms_code.delay(mobile, data_code)
        # 7.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

