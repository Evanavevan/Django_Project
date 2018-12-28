from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),

    # 上传文件
    url(r'^upfile/$', views.upfile),
    url(r'^savefile/$', views.savefile),

    # 分页显示
    url(r'^studentpage/(\d+)/$', views.studentpage),

    # ajax显示
    url(r'^ajax/$', views.ajax),
    url(r'^studentsinfo/$', views.studentsinfo),

    # 富文本显示
    url(r'^edit/$', views.edit),
    url(r'^saveedit/$', views.saveedit),

]