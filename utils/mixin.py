# -*- coding:utf-8 -*-
# @Desc : LoginRequiredMixin类使用
# @Author : Administrator
# @Date : 2019-01-16 15:57

# 实现项目中只有登陆后才能访问某些网页的限制功能
# 访问不登录就不能访问的页面时自动跳转到登陆页面

from django.contrib.auth.decorators import login_required

# 1.编写一个类,复写as_view方法,并调用父类的as_view方法
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin,cls).as_view(**initkwargs)
        # print(view,type(view))
        return login_required(view)

# 2.在需要做限制的类视图中继承1.中的自定义类



