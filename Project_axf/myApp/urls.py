from django.conf.urls import url
from . import views

urlpatterns = {
    # 主页
    url(r'^home/$', views.home, name='home'),

    # 超市
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),

    # 购物车
    url(r'^shoppingcar/$', views.shopping_car, name='shopping_car'),
    # 修改购物车，包括添加商品，添加减小商品数量
    url(r'^changeshoppingcar/(\d+)/$', views.change_shopping_car, name='change_shopping_car'),
    # 修改订单信息
    url(r'^changeinfo/$', views.change_info, name='change_info'),
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
    # 待付款
    url(r'^mine/orderWaitPay/$', views.order_wait_pay, name='order_wait_pay'),
    # 立即付款
    url(r'^mine/userPayOrder/(\d+)/$', views.user_pay_order, name='user_pay_order'),
    # 查看全部订单
    url(r'^mine/checkAllOrder/$', views.check_all_order, name='check_all_order'),
    # 待收货
    url(r'^mine/waitReceiveProduct/$', views.wait_receive_product, name='wait_receive_product'),

}