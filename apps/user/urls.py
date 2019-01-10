from django.conf.urls import url
from apps.user import views


urlpatterns = [

    url(r'^register$', views.register, name='register'),  # 显示注册页面  # 显示注册页面和处理注册用户请求
    # url(r'^register_handle$', views.register_handle, name='register_handle'),  # 显示注册页面
    # url(r'^registerview$',views.RegisterView.as_view(),name='registerview'),  # 使用类视图处理用户注册请求


]
