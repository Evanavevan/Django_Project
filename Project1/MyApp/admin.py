from django.contrib import admin

# Register your models here.
from .models import Grades, Students


# 注册
# 此类是为了创建新班级的时候附带输入两个学生的信息
class StudentInfo(admin.TabularInline):
    model = Students
    extra = 2


@admin.register(Grades)
class GradeAdmin(admin.ModelAdmin):
    # 关联对象
    inlines = [StudentInfo]
    # 列表页属性
    list_display = ['pk', 'gname', 'gdate', 'ggirlnum', 'gboynum', 'isDelete']  # 显示字段，类似于数据库的list
    list_filter = ['gname']     # 过滤器
    search_fields = ['gname']   # 搜索栏
    list_per_page = 2   # 分页

    # 添加修改页属性
    # fields =
    fieldsets = [
        ('base', {'fields': ['gname', 'gdate', 'isDelete']}),
        ('num', {'fields': ['ggirlnum', 'gboynum']})
    ]
# admin.site.register(Grades, GradeAdmin)


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    def gender(self):
        if self.sgender:
            return '男'
        else:
            return '女'

    def Delete(self):
        if self.isDelete:
            return '是'
        else:
            return '否'
    # gender.short_description = '性别'
    # 列表页属性
    list_display = ['pk', 'sname', gender, 'sage', 'sintroduction', 'sgrade', Delete]  # 显示字段，类似于数据库的list
    list_filter = ['sname', 'sage', 'sgrade']     # 过滤器
    search_fields = ['sname', 'sage', 'sgrade']   # 搜索栏
    list_per_page = 4   # 分页

    # 添加修改页属性
    # fields =
    fieldsets = [
        ('base', {'fields': ['sname', 'sgender', 'sage']}),
        ('other', {'fields': ['sintroduction', 'sgrade', 'isDelete']})
    ]
# admin.site.register(Students, StudentAdmin)
