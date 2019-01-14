from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired  # 过期异常

from apps.user.models import User
import re


# /user/register
def register(request):
    '''显示注册页面和处理注册用户请求'''
    if request.method == 'GET':
        # 显示注册页面
        return render(request, 'register.html')
    else:  # 处理注册请求
        # 获取注册请求参数
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # print(allow)

        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errormessage': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormessage': '邮箱格式不正确'})

        # 校验是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'errormessage': '请同意协议'})

        # 验证要注册的用户是否已经存在,get()当查不到数据时会抛出异常
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 说明用户不存在
            user = None
        if user:  # 用户名已经存在
            return render(request, 'register.html', {'errormessage': '用户名已经存在'})

        # 业务处理,进行用户注册
        user = User.objects.create_user(username, password, email)  # 默认账号注册后是激活状态
        user.is_active = 0  # 设置用户不是激活状态
        user.save()

        # 发送激活邮件,包含激活链接地址: http://127.0.0.0:8000/user/active/3
        # 激活链接中需要包含用户的身份信息,并且要把身份信息加密

        # 加密用户的身份信息,生成激活token,使用django中settings.py文件中的SECRET_KEY字符串信息
        from django.conf import settings
        serializer = Serializer(settings.SECRET_KEY, 3600)  # 设置一小时后过期
        info = {"confirm": user.id}  # 用户的id,唯一性
        token = serializer.dumps(info)  # 加密身份信息

        # 给注册用户发送邮件
        subject = '天天生鲜欢迎信息'  # 邮件标题信息
        # 邮件正文内容,message不能解析html信息,所以使用:html_message
        message = ''
        html_message = '<h1>%s,欢迎你成为天天生鲜注册会员,</h1>请点击下面链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
            username, token, token)
        from_email = settings.EMAIL_FROM  # 发件人件人邮箱
        recipient_list = [email]  # 收件人邮箱列表
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        # 返回应答,跳转到主页
        return redirect(reverse('goods:index'))

# /user/register_handle
def register_handle(request):
    '''处理注册请求'''
    # 获取注册请求参数
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    # print(allow)

    # 进行数据校验
    if not all([username, password, email]):
        return render(request, 'register.html', {'errormessage': '数据不完整'})

    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errormessage': '邮箱格式不正确'})

    # 校验是否同意协议
    if allow != 'on':
        return render(request, 'register.html', {'errormessage': '请同意协议'})

    # 验证要注册的用户是否已经存在,get()当查不到数据时会抛出异常
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 说明用户不存在
        user = None
    if user:  # 用户名已经存在
        return render(request, 'register.html', {'errormessage': '用户名已经存在'})

    # 业务处理,进行用户注册
    user = User.objects.create_user(username, password, email)  # 默认账号注册后是激活状态
    user.is_active = 0  # 设置为不是激活状态
    user.save()

    # 返回应答,跳转到主页
    return redirect(reverse('goods:index'))

# /user/register
class RegisterView(View):
    '''使用类视图显示注册页面和处理注册用户请求'''
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 获取注册请求参数
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # print(allow)

        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errormessage': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormessage': '邮箱格式不正确'})

        # 校验是否同意协议
        if allow != 'on':
            return render(request, 'register.html', {'errormessage': '请同意协议'})

        # 验证要注册的用户是否已经存在,get()当查不到数据时会抛出异常
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 说明用户不存在
            user = None
        if user:  # 用户名已经存在
            return render(request, 'register.html', {'errormessage': '用户名已经存在'})

        # 业务处理,进行用户注册
        user = User.objects.create_user(username, password, email)  # 默认账号注册后是激活状态
        user.is_active = 0  # 设置为不是激活状态
        user.save()

        # 发送激活邮件,包含激活链接地址: http://127.0.0.0:8000/user/active/3
        # 激活链接中需要包含用户的身份信息,并且要把身份信息加密

        # 加密用户的身份信息,生成激活token,使用django中settings.py文件中的SECRET_KEY字符串信息
        from django.conf import settings
        serializer = Serializer(settings.SECRET_KEY, 3600)  # 设置一小时后过期
        info = {"confirm": user.id}  # 用户的id,唯一性
        token = serializer.dumps(info)  # 加密身份信息,数据类型为bytes类型
        token = token.decode()  # 把bytes数据转换成字符串类型数据,decode()默认是utf-8

        # 给注册用户发送邮件
        subject = '天天生鲜欢迎信息'  # 邮件主题信息
        # 邮件正文内容,message不能解析html信息,所以需要使用:html_message
        message = ''
        from_email = settings.EMAIL_FROM  # 发件人邮箱
        recipient_list = [email]  # 收件人邮箱列表
        html_message = '<h1>%s,欢迎你成为天天生鲜注册会员,</h1>请点击下面链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)
        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        # 返回应答,跳转到主页
        return redirect(reverse('goods:index'))

# /user/active
class ActiveView(View):
    '''用户激活 - 类视图'''
    def get(self, request, token):
        # 进行解密,获取要激活的用户
        from django.conf import settings
        serializer = Serializer(settings.SECRET_KEY, 3600)  # 跟加密设置一致
        try:
            result = serializer.loads(token)  # 解密信息
            user_id = result['confirm']  # 获取待激活用户的id
            user = User.objects.get(id=user_id)  # 根据用户id获取用户信息
            user.is_active = 1  # 设置用户的状态为激活状态 1
            user.save()

            # 激活成功后,跳转到登陆页面
            return redirect(reverse('user:login'))

        except SignatureExpired as s:
            # 激活链接已过期
            return HttpResponse("激活链接已过期")

# /user/login
class LoginView(View):
    '''登陆'''
    def get(self, request):
        '''显示登陆页面'''
        return render(request, 'login.html')







