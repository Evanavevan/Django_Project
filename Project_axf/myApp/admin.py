from django.contrib import admin
from .models import Wheel, Nav, Mustbuy, Shop, Show, FoodTypes, Products, User, Cart, Order

# Register your models here.


@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''
    # 列表页属性
    list_display = ['pk', 'img', 'name', 'trackid', Delete]  # 显示字段，类似于数据库的list
    list_filter = ['isDelete']     # 过滤器
    search_fields = ['name', 'trackid']   # 搜索栏
    list_per_page = 10   # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(Nav)
class NavAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''

    # 列表页属性
    list_display = ['pk', 'img', 'name', 'trackid', Delete]  # 显示字段，类似于数据库的list
    list_filter = ['isDelete']  # 过滤器
    search_fields = ['name', 'trackid']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(Mustbuy)
class MustbuyAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''

    # 列表页属性
    list_display = ['pk', 'img', 'name', 'trackid', Delete]  # 显示字段，类似于数据库的list
    list_filter = ['isDelete']  # 过滤器
    search_fields = ['name', 'trackid']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''

    # 列表页属性
    list_display = ['pk', 'img', 'name', 'trackid', Delete]  # 显示字段，类似于数据库的list
    list_filter = ['isDelete']  # 过滤器
    search_fields = ['name', 'trackid']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['pk', 'img', 'name', 'trackid', 'categoryid', 'brandname', 'img1', 'childcid1', 'productid1',
                    'longname1', 'price1', 'marketprice1', 'img2', 'childcid2', 'productid2', 'longname2', 'price2',
                    'marketprice2', 'img3', 'childcid3', 'productid3', 'longname3', 'price3', 'marketprice3']
    list_filter = ['categoryid', 'brandname']  # 过滤器
    search_fields = ['name', 'trackid']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(FoodTypes)
class FoodTypesAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['pk', 'typeid', 'typename', 'typesort', 'childtypenames']  # 显示字段，类似于数据库的list
    list_filter = ['typename']  # 过滤器
    search_fields = ['typeid', 'typename']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    def isXF(self):
        if self.isxf:
            return '是'
        else:
            return '否'
    def isPmdesc(self):
        if self.pmdesc == '1':
            return '是'
        else:
            return '否'
    # 列表页属性
    list_display = ['pk', 'productid', 'productimg', 'productname', 'productlongname', isXF, isPmdesc, 'specifics',
                    'price', 'marketprice', 'categoryid', 'childcid', 'childcidname', 'dealerid', 'storenums',
                    'productnum']
    list_filter = ['isxf', 'pmdesc', 'childcidname']  # 过滤器
    search_fields = ['productid', 'productlongname', 'childcid']  # 搜索栏
    list_per_page = 100  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('base', {'fields': ['img', 'name', 'trackid', 'isDelete']})
    # ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['pk', 'userAccount', 'userPassword', 'userName', 'userPhonenumber', 'userAddress', 'userImg',
                    'userRank', 'userToken']
    list_filter = ['userRank']  # 过滤器
    search_fields = ['userAccount', 'userName', 'userPhonenumber', 'userAddress', 'userRank']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    fieldsets = [
        ('', {'fields': ['userAccount', 'userPassword', 'userName', 'userPhonenumber', 'userAddress', 'userImg',
                         'userRank']})
    ]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''
    def chose(self):
        if self.isChose:
            return '√'
        else:
            return ''
    # 列表页属性
    list_display = ['pk', 'userAccount', 'productid', 'productnum', 'productprice', chose, 'productimg', 'productname',
                    'orderid', Delete]
    list_filter = ['userAccount', 'productname', 'isChose', 'isDelete']  # 过滤器
    search_fields = ['userAccount', 'productid', 'productname', 'orderid']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('', {'fields': ['userAccount', 'userPassword', 'userName', 'userPhonenumber', 'userAddress', 'userImg',
    #                      'userRank']})
    # ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def Delete(self):
        if self.isDelete:
            return '√'
        else:
            return ''
    def chose(self):
        if self.isChose:
            return '√'
        else:
            return ''
    # 列表页属性
    list_display = ['pk', 'orderid', 'userid', 'receiver', 'phonenum', 'receiveaddress', 'money', 'progress']
    list_filter = ['userid', 'receiver', 'progress']  # 过滤器
    search_fields = ['orderid', 'userid', 'receiver', 'phonenum', 'receiveaddress', 'money', 'progress']  # 搜索栏
    list_per_page = 10  # 分页

    # 添加修改页属性
    # fieldsets = [
    #     ('', {'fields': ['userAccount', 'userPassword', 'userName', 'userPhonenumber', 'userAddress', 'userImg',
    #                      'userRank']})
    # ]
