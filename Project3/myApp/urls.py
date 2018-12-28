from django.conf.urls import url

from . import views, verifycode

urlpatterns = [
    # url(r'^$', views.index),
    # 生成验证码
    url(r'^verifycode/$', verifycode.Verifycode),

    # 输入验证码试验
    url(r'^verifycodeinput/$', views.verifycodeinput),
    url(r'^verifycodecheck/$', views.checkcode),

    # 反向解析（针对的是超链接，千万别弄错）
    # 成功的
    # url(r'^$', views.student),
    # url(r'^return/(\d+)/$', views.retu, name='return'),

    # 一开始不成功，上面成功后就成功
    url(r'^student/$', views.student),
    url(r'^student/return/(\d+)/$', views.retu, name='return'),


    # 模板继承
    url(r"^main/$", views.main),
]