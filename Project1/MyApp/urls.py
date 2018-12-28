from django.conf.urls import url
from . import views

#编写url尤其注意正则表达式匹配字符串的结尾，否则会引起冲突而达不到理想中的效果
urlpatterns = [
    url(r'^$', views.index),
    url(r'^(\d+)/$', views.detail),

    url(r'^grades/$', views.grades),
    url(r'^students/$', views.students),
    url(r'^grades/(\d+)$', views.gradeStudents),


    url(r'^addstudent/$', views.addstudent)
]