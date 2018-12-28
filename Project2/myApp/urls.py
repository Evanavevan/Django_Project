from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^students/$', views.students),

    #测试网址：http://127.0.0.1:8000/get1?a=1&b=2&c=3
    url(r'^get1/$', views.get1),
    #测试网址：http://127.0.0.1:8000/get2?a=1&a=2&c=3
    url(r'^get2/$', views.get2),

    #Post属性
    url(r'^registerpage/$', views.registerpage),
    url(r'^registerpage/register/$', views.register),
    url(r'^^registerpage/register/return/$', views.return_),

    #回话实例
    url(r'^mainpage/$', views.mainpage),
    url(r'^login/$', views.login),
    url(r'^login/showmainpage/$', views.showmainpage),
    url(r'^logout/$', views.logout_),

]

