from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r'^home/$', views.home, name='home'),

    # 超市
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),


    # 购物车
    url(r'^shoppingcar/$', views.shoppingcar, name='shoppingcar'),
    # 修改购物车，包括添加商品，添加减小商品数量
    url(r'^changeshoppingcar/(\d+)/$', views.changeshoppingcar, name='changeshoppingcar'),
    # 修改订单信息
    url(r'^changeinfo/$', views.changeinfo, name='changeinfo'),
    # 提交订单
    url(r'^saveorder/$', views.order, name='order'),


    # 我的
    url(r'^mine/$', views.mine, name='mine'),
    # 登录界面
    url(r'^login/$', views.login, name='login'),
    # 注册界面
    url(r'^register/$', views.register, name='register'),
    # 验证用户是否注册
    url(r'^checkuserid/$', views.checkuserid, name='checkuserid'),
    # 退出登录
    url(r'^logout/$', views.logout, name='logout'),


]