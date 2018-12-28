from django.shortcuts import render, redirect

# Create your views here.
from .models import Wheel, Nav, Mustbuy, Shop, Show, FoodTypes, Products, User, Cart, Order
import os
import time
import random
from django.conf import settings
from .forms.login import LoginForm
from django.http import JsonResponse


# 主页
def home(request):
    # 轮播信息列表
    wheelList = Wheel.objects.all()
    # 导航信息列表
    navList = Nav.objects.all()
    # 推荐信息列表
    recommendList = Mustbuy.objects.all()
    # 种类汇总列表
    shopList = Shop.objects.all()
    # 便利店
    shop1 = shopList[0]
    # 热销榜和新品尝鲜
    shop2 = shopList[1:3]
    # 分类导航
    shop3 = shopList[3:7]
    # 推荐
    shop4 = shopList[7:]
    # 具体商品展示列表
    showList = Show.objects.all()
    return render(request, 'myApp/home.html', {'Title': '主页', 'wheelList': wheelList, 'navList': navList,
                                               'recommendList': recommendList, 'shop1': shop1, 'shop2': shop2,
                                               'shop3': shop3, 'shop4': shop4, 'showList': showList})


# 超市
def market(request, categoryid, cid, sortid):
    # 种类栏列表
    leftSlider = FoodTypes.objects.all()

    # 筛选
    # 全部分类，保持页面不刷新
    if cid == '0':
        productList = Products.objects.filter(categoryid=categoryid)
    else:
        productList = Products.objects.filter(categoryid=categoryid, childcid=cid)

    # 排序
    # 销量排序，降序
    if sortid == '1':
        # “-”表示降序排列
        productList = productList.order_by('-productnum')
    # 价格降序
    elif sortid == '2':
        productList = productList.order_by('-price')
    # 价格升序
    elif sortid == '3':
        productList = productList.order_by('price')

    # 点击类型分类
    group = leftSlider.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split('#')
    for s in arr1:
        arr2 = s.split(':')
        obj = {'childname': arr2[0], 'childId': arr2[1]}
        childList.append(obj)

    # 显示商品数字
    cartList = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken=token)
        cartList = Cart.objects.filter(userAccount=user.userAccount)
    for p in productList:
        for c in cartList:
            if p.productid == c.productid:
                p.num = c.productnum
                continue

    return render(request, 'myApp/market.html', {'Title': '超市', 'leftSlider': leftSlider, 'productList': productList,
                                                 'childList': childList, 'categoryid': categoryid, "cid": cid})


# 购物车
def shoppingcar(request):
    token = request.session.get("token")
    cartslist = []
    user = None
    trueFlag = 0
    count = 0
    totalprice = 0
    # 用户已登录
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount=user.userAccount)
        for item in cartslist:
            if item.isChose == False:
                count += 1
            else:
                # 计算购物车总价
                totalprice += float(item.productprice)
        if count == 0:
            trueFlag = 1
        if len(cartslist) == 0:
            trueFlag = 0
    return render(request, 'myApp/shoppingcar.html', {'Title': '购物车', 'cartslist': cartslist, 'user': user,
                                                      'trueFlag': trueFlag, "sum": totalprice})


# 修改购物车
def changeshoppingcar(request, flag):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        # 没登录
        # 用a-jax无法重定向
        # return redirect("/login/")
        return JsonResponse({"data": -1, "status": "error"})
    else:
        user = User.objects.get(userToken=token)
        try:
            # 获取ajax提交的信息
            productid = request.POST.get("productid")
            product = Products.objects.get(productid=productid)
        except:
            # 获取ajax提交的全选框的状态信息
            allchose = request.POST.get("allchose")
        totalprice = 0
        if flag == '0':
            # 判断商品库存
            if product.storenums == 0:
                # 数量达到库存量，无论怎样点击+号，也没任何反应
                return JsonResponse({"data": -2, "status": "error"})
            carts = Cart.objects.filter(userAccount=user.userAccount)
            try:
                # 商品如果加入了购物车，点击+号增加数量
                c = carts.get(productid=productid)
                # 修改数量和总价
                c.productnum += 1
                c.productprice = "%.2f" % (product.price*c.productnum)
                c.save()
            except Cart.DoesNotExist:
                # 没有添加此商品直接增加一条订单
                c = Cart.createuser(user.userAccount, productid, 1, product.price, True, product.productimg,
                                    product.productlongname, False)
                c.save()
            # 库存减一
            product.storenums -= 1
            product.save()
            # 计算购物车总价钱
            cartList = Cart.objects.filter(userAccount=user.userAccount)
            for item in cartList:
                totalprice += float(item.productprice)
            return JsonResponse({"data": c.productnum, "price": c.productprice, "sum": totalprice, "status": "success"})
        elif flag == '1':
            carts = Cart.objects.filter(userAccount=user.userAccount)
            try:
                # 商品如果加入了购物车，点击-号才有效
                c = carts.get(productid=productid)
                # 修改数量和总价
                c.productnum -= 1
                c.productprice = "%.2f" % (product.price*c.productnum)
                # 数量减为0删除订单
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist:
                # 商品没有加入到购物车，无论怎样点击-号，都没有反应
                return JsonResponse({"data": -2, "status": "error"})
            # 库存加一
            product.storenums += 1
            product.save()
            # 计算购物车总价钱
            cartList = Cart.objects.filter(userAccount=user.userAccount)
            for item in cartList:
                totalprice += float(item.productprice)
            return JsonResponse({"data": c.productnum, "price": c.productprice, "sum": totalprice, "status": "success"})
        elif flag == "2":
            carts = Cart.objects.filter(userAccount=user.userAccount)
            c = carts.get(productid=productid)
            c.isChose = not c.isChose
            c.save()
            s = ''
            a = ''
            count = 0
            if c.isChose:
                s = "√"
            # 计算购物车总价钱
            cartList = Cart.objects.filter(userAccount=user.userAccount)
            for item in cartList:
                if item.isChose == True:
                    totalprice += float(item.productprice)
                else:
                    count += 1
            # 改变全选框的状态
            if count == 0:
                a = "√"
            return JsonResponse({"data": s, "all": a, "sum": totalprice, "status": "success"})
        elif flag == '3':
            cartsList = Cart.objects.filter(userAccount=user.userAccount)
            # 如果全选框中的内容为空，则点击后会打上勾，以上清单列表的商品也要全部打上勾
            if allchose == "":
                for item in cartsList:
                    item.isChose = True
                    item.save()
                s = "√"
            # 如果全选框中的内容为√，则点击后会取消勾，以上清单列表的商品也要全部取消勾
            elif allchose == "√":
                for item in cartsList:
                    item.isChose = False
                    item.save()
                s = ""
            # 计算购物车总价钱
            cartList = Cart.objects.filter(userAccount=user.userAccount)
            for item in cartList:
                if item.isChose == True:
                    totalprice += float(item.productprice)
            return JsonResponse({"data": s, "sum": totalprice, "status": "success"})


# 提交订单
def order(request):
    token = request.session.get("token")
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose=True)
    if carts.count() == 0:
        return JsonResponse({"data": -1, "status": "error"})
    # 计算总价
    summoney = 0
    for pro in carts:
        summoney += pro.productnum * float(pro.productprice)
    oid = time.time() + random.randrange(1, 10000)
    oid = "%d" % oid
    try:
        # 取出修改的信息
        name = request.session["name"]
        phonenum = request.session["phonenum"]
        address = request.session["address"]
        o = Order.createorder(oid, user.userAccount, name, phonenum, address, summoney, 0)
    except:
        o = Order.createorder(oid, user.userAccount, user.userName, user.userPhonenumber, user.userAddress,
                              summoney, 0)
    o.save()
    for item in carts:
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({"status": "success"})


# 修改订单信息
def changeinfo(request):
    if request.method == "POST":
        count = 0
        trueFlag = 0
        # 获取修改的信息
        name = request.POST.get('receiver')
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        # 将修改的信息存进session中
        request.session["name"] = name
        request.session["phonenum"] = phonenumber
        request.session["address"] = address

        # 获取用户加入购物车的商品
        token = request.session.get("token")
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount=user.userAccount)
        # 判断全部商品是否都选中了，如果全选中，全选框也要打上勾
        for item in cartslist:
            if item.isChose == False:
                count += 1
                break
        if count == 0:
            trueFlag = 1
        # 清单列表为空全选框也要为空
        if len(cartslist) == 0:
            trueFlag = 0
        return render(request, "myApp/shoppingcar.html", {'Title': '购物车', 'cartslist': cartslist, 'user': user,
                                                          'trueFlag': trueFlag, "name": name, "phonenum": phonenumber,
                                                          "address": address})
    else:
        return render(request, "myApp/changeinfo.html", {'Title': '修改订单信息'})


# 我的
def mine(request):
    # 判断用户是否登录
    flag = 0
    token = request.session.get("token")
    if token:
        flag = 1
        username = request.session.get("username")
        user = User.objects.get(userName=username)
        return render(request, 'myApp/mine.html', {'Title': '我的', "username": username, 'flag': flag, 'user': user})
    else:
        username = ''
        return render(request, 'myApp/mine.html', {'Title': '我的', "username": username, 'flag': flag})


# 登录
def login(request):
    if request.method == 'POST':
        # 自定义表单
        form = LoginForm(request.POST)
        if form.is_valid():
            # 信息格式没有问题，验证账号和密码的正确性
            # 表单的内容存放在cleaned_data中
            name = form.cleaned_data['username']
            pswd = form.cleaned_data['password']
            try:
                user = User.objects.get(userAccount=name)
                # 密码不对
                if user.userPassword != pswd:
                    return redirect('/login/')
            # 用户不存在
            except User.DoesNotExist:
                return redirect('/login/')

            # 登录成功更换token值
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            # 存储信息显示
            request.session['username'] = user.userName
            request.session['token'] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'myApp/login.html', {'Title': '登录', "form": form, 'error': form.errors})
    else:
        f = LoginForm()
        return render(request, 'myApp/login.html', {'Title': '登录', "form": f})


# 注册
def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPasswd")
        userName = request.POST.get("userName")
        userPhonenumber = request.POST.get("userPhonenumber")
        userAddress = request.POST.get("userAddress")
        userRank = 0

        # 创建token，一个随机分配的值
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)

        # 头像
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MEDIA_ROOT, userAccount+'.png')
        with open(userImg, 'wb') as fp:
            for i in f.chunks():
                fp.write(i)

        user = User.createuser(userAccount, userPasswd, userName, userPhonenumber, userAddress, userImg, userRank,
                               userToken)
        user.save()

        # 存储信息显示
        request.session['username'] = userName
        request.session['token'] = userToken

        return redirect('/mine/')
    else:
        return render(request, 'myApp/register.html', {'Title': '注册'})


# 验证用户是否存在
def checkuserid(request):
    userid = request.POST.get('userid')
    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data": "该用户已注册", 'status': 'error'})
    except User.DoesNotExist:
        return JsonResponse({"data": '该用户还没注册', 'status': 'success'})


# 退出登录
# from django.contrib.auth import logout
def logout(request):
    # 使用logout会显示超时
    # logout(request)
    request.session.clear()
    return redirect('/mine/')
