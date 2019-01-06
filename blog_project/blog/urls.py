from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^index/$', index, name='index'),
    # 存档
    url(r'^archive/', archive, name='archive'),
    # 文章详情
    url(r'^article/', passage, name='article'),
    # 提交评论
    url(r'^comment/post/$', comment_post, name='comment_post'),
    # 注销
    url(r'^logout/$', do_logout, name='logout'),
    # 注册
    url(r'^reg/$', do_reg, name='reg'),
    # 登录
    url(r'^login/$', do_login, name='login'),
    # 导航栏分类
    url(r'^category/', category, name='category'),
    # 标签
    url(r'^tag/', tag, name='tag'),
]
