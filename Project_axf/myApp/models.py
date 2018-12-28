from django.db import models

# Create your models here.


# 主页
# 最上面的滑动条
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)


# 导航页
class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)


# 每日推荐
class Mustbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)


# 分类总页展示
class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)


# 具体商品信息
class Show(models.Model):
    trackid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=20)
    productid1 = models.CharField(max_length=20)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=20)
    marketprice1 = models.CharField(max_length=20)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=20)
    productid2 = models.CharField(max_length=20)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=20)
    marketprice2 = models.CharField(max_length=20)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=20)
    productid3 = models.CharField(max_length=20)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=20)
    marketprice3 = models.CharField(max_length=20)


# 闪送超市
# 商品分类
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField()
    childtypenames = models.CharField(max_length=150)


# 具体商品模型类
class Products(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=150)
    # 商品短名称
    productname = models.CharField(max_length=50)
    # 商品长名称
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.NullBooleanField(default=False)
    # 是否买一送一
    pmdesc = models.CharField(max_length=10)
    # 规格
    specifics = models.CharField(max_length=20)
    # 价格
    price = models.FloatField()
    # 市场价格
    marketprice = models.FloatField()
    # 分类id
    categoryid = models.CharField(max_length=10)
    # 子类组id
    childcid = models.CharField(max_length=10)
    # 子类组名称
    childcidname = models.CharField(max_length=10)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()


# 用户注册模型类
class User(models.Model):
    # 用户账号，唯一
    userAccount = models.CharField(max_length=20, unique=True)
    # 密码
    userPassword = models.CharField(max_length=20)
    # 姓名
    userName = models.CharField(max_length=20)
    # 手机号
    userPhonenumber = models.CharField(max_length=20)
    # 地址
    userAddress = models.CharField(max_length=100)
    # 头像路径
    userImg = models.CharField(max_length=150)
    # 等级
    userRank = models.IntegerField()
    # token验证值，每次登录之后都会更新
    userToken = models.CharField(max_length=50)

    @classmethod
    def createuser(cls, account, password, name, phonenumber, address, img, rank, token):
        u = cls(userAccount=account, userPassword=password, userName=name, userPhonenumber=phonenumber,
                userAddress=address, userImg=img, userRank=rank, userToken=token)
        return u


# 自定义管理器
# 用于在购物车中点击提交订单后显示不打钩的商品
class CartManager1(models.Manager):
    def get_queryset(self):
        return super(CartManager1, self).get_queryset().filter(isDelete=False)


# 购物车清单模型
class Cart(models.Model):
    # 用户账号，唯一
    userAccount = models.CharField(max_length=20, unique=False)
    # 商品id
    productid = models.CharField(max_length=10)
    # 商品数量
    productnum = models.IntegerField()
    # 商品价格
    productprice = models.CharField(max_length=10)
    # 是否被选中
    isChose = models.BooleanField(default=True)
    # 商品图片
    productimg = models.CharField(max_length=150)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 订单ID
    orderid = models.CharField(max_length=20, default="0")
    # 是否删除
    isDelete = models.BooleanField(default=False)

    objects = CartManager1()

    @classmethod
    def createuser(cls, account, id, num, price, isChose, img, name, isDelete):
        c = cls(userAccount=account, productid=id, productnum=num, productprice=price, isChose=isChose, productimg=img,
                productname=name, isDelete=isDelete)
        return c


# 订单模型
class Order(models.Model):
    # 订单号
    orderid = models.CharField(max_length=20)
    # 用户名
    userid = models.CharField(max_length=20)
    # 收货人
    receiver = models.CharField(max_length=20, default="")
    # 手机号码
    phonenum = models.CharField(max_length=20)
    # 收货地址
    receiveaddress = models.CharField(max_length=50, default="")
    # 订单金额
    money = models.FloatField(default=0)
    # 进程
    progress = models.IntegerField()

    @classmethod
    def createorder(cls, orderid, userid, receiver, phonenum, receiveaddress, money, progress):
        o = cls(orderid=orderid, userid=userid, receiver=receiver, phonenum=phonenum, receiveaddress=receiveaddress,
                money=money,progress=progress)
        return o
