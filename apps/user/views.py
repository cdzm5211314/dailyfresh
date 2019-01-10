from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from apps.user.models import User
import re


# Create your views here.

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
        user = User.objects.create_user(username, password, email)  # 默认是账号注册后是激活状态
        user.is_active = 0  # 设置为不是激活状态
        user.save()

        # 返回应答,跳转到主页
        return redirect(reverse('goods:index'))

"""
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
    user = User.objects.create_user(username, password, email)  # 默认是账号注册后是激活状态
    user.is_active = 0  # 设置为不是激活状态
    user.save()

    # 返回应答,跳转到主页
    return redirect(reverse('goods:index'))
"""











