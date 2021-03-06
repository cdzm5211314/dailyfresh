from django.conf.urls import url
# from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView, LogoutView,UserInfoView, UserOrderView, AddressView
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # url(r'^register$', views.register, name='register'),  # 显示注册页面  # 显示注册页面和处理注册用户请求
    # url(r'^register_handle$', views.register_handle, name='register_handle'),  # 显示注册页面

    url(r'^register$', RegisterView.as_view(), name='register'),  # 使用类视图处理用户注册请求
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 使用类视图处理用户激活

    url(r'^login$', LoginView.as_view(), name='login'),  # 使用类视图处理用户登陆
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 使用类视图处理用户退出

    # 用户中心页面需要用户登陆后才能访问,可以使用django内置的login_required登陆装饰器
    # url(r'^$', login_required(UserInfoView.as_view()), name='user'),  # 使用类视图处理用户中心-信息页
    # url(r'^order$', login_required(UserOrderView.as_view()), name='order'),  # 使用类视图处理用户中心-订单页
    # url(r'^address$', login_required(AddressView.as_view()), name='address'),  # 使用类视图处理用户中心-地址页

    # 用户中心页面需要用户登陆后才能访问,可以编写utilt.LoginRequiredMixin类来继承实现
    url(r'^$', UserInfoView.as_view(), name='user'),  # 使用类视图处理用户中心-信息页
    url(r'^order$', UserOrderView.as_view(), name='order'),  # 使用类视图处理用户中心-订单页
    url(r'^address$', AddressView.as_view(), name='address'),  # 使用类视图处理用户中心-地址页

]
