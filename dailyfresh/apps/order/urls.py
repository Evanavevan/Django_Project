from django.conf.urls import url
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, CommentView, UnionPayView, WeiXinPay

urlpatterns = [
    url(r'^place$', OrderPlaceView.as_view(), name='place'),  # 提交订单页面显示
    url(r'^commit$', OrderCommitView.as_view(), name='commit'),  # 订单创建
    url(r'^pay$', OrderPayView.as_view(), name='pay'),  # 订单支付
    url(r'^check$', CheckPayView.as_view(), name='check'),  # 查询支付交易结果
    url(r'^comment/(?P<order_id>.+)$', CommentView.as_view(), name='comment'),  # 订单评论
    url(r'^unionpay$', UnionPayView.as_view(), name='union_pay'),  # 银联支付
    url(r'^weixinpay$', WeiXinPay.as_view(), name='weixin_pay'),  # 微信支付
]
