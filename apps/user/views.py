from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired  # 过期异常

from celery_tasks.tasks import send_register_active_email  # 使用celery异步发送邮件
from apps.user.models import User, Address
from apps.goods.models import GoodsSKU
from utils.mixin import LoginRequiredMixin
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
        # user = User.objects.create_user(username, email, password)  # 默认账号注册后是激活状态
        user = User.objects.create_user(username=username, email=email, password=password)  # 默认账号注册后是激活状态
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

        # 给注册用户发送邮件:
        from celery_tasks.tasks import send_register_active_email  # 使用celery异步发送邮件
        send_register_active_email.delay(email, username, token)  # 发出任务

        # 给注册用户发送邮件:
        # subject = '天天生鲜欢迎信息'  # 邮件主题信息
        # # 邮件正文内容,message不能解析html信息,所以需要使用:html_message
        # message = ''
        # from_email = settings.EMAIL_FROM  # 发件人邮箱
        # recipient_list = [email]  # 收件人邮箱列表
        # html_message = '<h1>%s,欢迎你成为天天生鲜注册会员,</h1>请点击下面链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        #     username, token, token)
        # send_mail(subject, message, from_email, recipient_list, html_message=html_message)

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
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'  # ???
        else:
            username = ''
            checked = ''  # ???
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''用户登陆校验'''
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 用户名与密码校验
        if not all([username, password]):
            return render(request, 'login.html', {'errormessage': '数据不完整'})

        # 登陆校验: 使用django内置的认证系统
        # user = authenticate(username="root1", password="12345678")  # 认证成功返回User对象,失败返回None
        user = authenticate(username=username, password=password)  # 认证成功返回User对象,失败返回None
        # print(user)
        if user is not None:  # 认证成功: 用户名和密码正确
            if user.is_active:  # 用户已激活
                login(request, user)  # 记录用户的登陆状态

                # 获取登陆后要跳转的地址
                # 默认跳转到首页
                # 如果是直接访问/user/login地址.next值为None,需要设置一个默认值
                next_url = request.GET.get('next', reverse('goods:index'))
                # print(next_url)
                response = redirect(next_url)  # 跳转到首页: HttpResponseRedirect

                # 判断用户是否记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':  # 已选中记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')
                return response  # 跳转到首页

            # ??? 已注册但未激活用户进不来????
            # settings配置默认检查用户是否活跃状态is_axtive,不活跃返回None
            # AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
            # settings配置设置不检查用户的活跃状态is_active
            # AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
            else:  # 用户未激活
                return render(request, 'login.html', {'errormessage': '用户未激活...'})
        else:  # 认证失败: 用户名或密码错误
            return render(request, 'login.html', {'errormessage': '用户名或密码错误...'})


# /user/logout
class LogoutView(View):
    '''用户退出操作'''

    def get(self, request):
        # 消除用户的session信息
        logout(request)  # 退出登陆操作
        return redirect(reverse('goods:index'))  # 跳转到首页


# Django会给request对象添加一个属性request.user
# 如果用户未登录->user是AnonymousUser类的一个实例对象
# 如果用户登录->user是User类的一个实例对象
# request.user.is_authenticated() # 在模版也是存在的

# /user
class UserInfoView(LoginRequiredMixin, View):
    '''用户中心-信息页'''

    def get(self, request):
        # 获取用户地址信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取商品的历史用浏览记录
        # 1.使用原生的redis链接redis数据
        # from redis import StrictRedis
        # sr = StrictRedis(host="localhost", port='6379', db=1)
        # 2.使用redis配置的cache缓存进行链接
        from django_redis import get_redis_connection
        conn = get_redis_connection('default')

        # 组织redis数据库中key的值
        history_key = 'history_%d' % user.id

        # 根据redis中key的值获取最近浏览的5个商品的id
        sku_ids = conn.lrange(history_key, 0, 4)

        # 遍历获取用户浏览的商品信息
        goods_list = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_list.append(goods)
        # goods_list = [GoodsSKU.objects.get(pk=sku_id) for sku_id in sku_ids]
        # goods_list = GoodsSKU.objects.filter(id__in = sku_ids )

        # 组织上下文信息
        context = {'page': 'user', 'address': address, 'goods_list': goods_list}

        return render(request, 'user_center_info.html', context)
        # return render(request, 'user_center_info.html', {'page': 'user', 'address': address,'goods_list':goods_list})


# /user/order
class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''

    def get(self, request):
        return render(request, 'user_center_order.html', {'page': 'order'})


# /user/address
class AddressView(LoginRequiredMixin, View):
    '''用户中心-地址页'''

    def get(self, request):
        '''获取用户默认地址'''
        # 获取登陆的用户信息
        user = request.user
        # print(user,type(user))  # django.utils.functional.SimpleLazyObject
        # try:
        #     # address = Address.objects.get(user=user, is_default=True)  # is_default = True 时,为默认收货地址
        #     # 上述获取登陆用户代码报错:
        #     # Cannot query "admin1": Must be "User" instance.   # admin1 <class 'django.utils.functional.SimpleLazyObject'>
        #     address = Address.objects.get(user_id=user.id, is_default=True)  # is_default = True 时,为默认收货地址
        # except Address.DoesNotExist:
        #     # 不存在默认的收货地址
        #     address = None

        # 使用模型管理器类封装方法来获取默认的收货地址
        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        '''添加地址信息'''
        # 获取提交的地址信息
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验提交数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg': '地址信息不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理:添加地址
        # 如果用户有默认收货地址,添加的地址就不作为默认的收货地址
        # 如果用户无默认收货地址,那添加的地址就作为默认的收货地址

        # 获取登陆的user对象
        user = request.user
        # try:
        #     # address = Address.objects.get(user=user, is_default=Te)  # is_default = True 时,为默认收货地址
        #     # 上诉获取登陆用户代码报错:
        #     # Cannot query "admin1": Must be "User" instance.   # admin1 <class 'django.utils.functional.SimpleLazyObject'>
        #     address = Address.objects.get(user_id=user.id, is_default=True)  # is_default = True 时,为默认收货地址
        # except Address.DoesNotExist:
        #     # 不存在默认的收货地址
        #     address = None

        # 使用模型管理器类封装方法来获取默认的收货地址
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        # Address.objects.create(user=user,receiver=receiver,zip_code=zip_code,phone=phone,is_default=is_default)
        # 以上代码报错:
        # ValueError: Cannot assign "<SimpleLazyObject: <User: admin1>>": "Address.user" must be a "User" instance.

        Address.objects.create(user_id=user.id, receiver=receiver, addr=addr, zip_code=zip_code, phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address'))
