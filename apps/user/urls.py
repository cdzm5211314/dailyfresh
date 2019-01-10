from django.conf.urls import url
# from apps.user import views
from apps.user.views import RegisterView,ActiveView,LoginView

urlpatterns = [

    # url(r'^register$', views.register, name='register'),  # 显示注册页面  # 显示注册页面和处理注册用户请求
    # url(r'^register_handle$', views.register_handle, name='register_handle'),  # 显示注册页面

    url(r'^register$',RegisterView.as_view(),name='register'),  # 使用类视图处理用户注册请求
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),  # 使用类视图处理用户激活
    url(r'^login$',LoginView.as_view(),name='login'),  # 使用类视图处理用户登陆


]
