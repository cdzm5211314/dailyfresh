# -*- coding:utf-8 -*-
# @Desc : 任务发出者
# @Author : Administrator
# @Date : 2019-01-14 14:50


# 任务处理者:(celery_tasks.tasks文件)加入如下内容:
# 加载django项目的配置信息
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DailyFresh.settings")
# 导入django,并启动django项目
# import django
# django.setup()

# 使用celery:结合redis数据库
# 1.Pyhon环境中(虚拟环境)需要安装: pip install celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner


# 2.创建Celery示例对象
# main参数: 随便写一个字符串,一般就写该文件的位置路径信息
# broker参数: 使用redis作为中间人,所以需要启动redis服务,需要redis数据库所在的ip地址,端口号及使用哪个数据库
# app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/2')  # redis无密码
app = Celery('celery_tasks.tasks',broker='redis://:password@192.168.208.128:6379/3')  # redis有密码

# 3.任务发起者:定义发出任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送注册用户激活邮件'''
    subject = '天天生鲜欢迎信息'  # 邮件主题信息
    # 邮件正文内容,message不能解析html信息,所以需要使用:html_message
    message = ''
    from_email = settings.EMAIL_FROM  # 发件人邮箱
    recipient_list = [to_email]  # 收件人邮箱列表
    html_message = '<h1>%s,欢迎你成为天天生鲜注册会员,</h1>请点击下面链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

## 任务处理者使用情况:
# 1.复制项目到本地电脑的另一个盘符中(windows)
# 2.进入项目根目录下执行命令: (dailyfresh) F:\DailyFresh>celery -A celery_tasks.tasks worker -l info
# 3.发现报错: 信息如下
# [2019-01-14 16:04:14,564: ERROR/MainProcess] consumer: Cannot connect to redis://127.0.0.1:6379/8: NOAUTH Authentication required..Trying again in 10.00 seconds...
# 4.windows下解决报错: 需要安装两个软件[RabbitMQ和Erlang]并配置环境变量
# Erlang: 下载地址: http://erlang.org/download/otp_win64_18.3.exe
# 设置系统变量名称: ERLANG_HOME=E:\InstallationOther\Erlang\erl7.3 然后加入path中: %ERLANG_HOME%\bin;
# RabbitMQ: 下载地址: http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server-3.6.9.exe
# 设置系统变量名称: RABBITMQ_SERVER=E:\InstallationOther\RabbitMQ\rabbitmq_server-3.6.9 然后加入path中: %RABBITMQ_SERVER%\sbin;
# 输入命令管理: "E:\InstallationOther\RabbitMQ\rabbitmq_server-3.6.9\sbin\rabbitmq-plugins.bat" enable rabbitmq_management
# 执行命令: net stop RabbitMQ && net start RabbitMQ
# 到安装目录sbin目录下执行: rabbitmqctl.bat add_user username password  # 创建用户,默认有个guest用户,密码一致
# 然后可以访问:  http://localhost:15672
# 启动RabbitMQ Server服务

# 如果接受任务时报错: 如 ValueError: not enough values to unpack (expected 3, got 0)
# 解决方法: 安装一个扩展 pip install eventlet
# 然后再启动celery: celery -A celery_tasks.tasks worker -l info -P eventlet


@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners}

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # 2.模板渲染
    static_index_html = temp.render(context)

    # 生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)


