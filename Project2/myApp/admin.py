from django.contrib import admin

# Register your models here.
from .models import Students, Grades


class StudentInfo(admin.TabularInline):
    model = Students
    extra = 2


@admin.register(Grades)
class GradeAdmin(admin.ModelAdmin):
    inlines = [StudentInfo]
    list_display = ['pk', 'gname', 'gdate', 'ggirlnum', 'gboynum', 'isDelete']
    list_filter = ['gname']
    search_fields = ['gname']
    list_per_page = 2
    fieldsets = [
        ('base', {'fields': ['gname', 'gdate', 'isDelete']}),
        ('num', {'fields': ['ggirlnum', 'gboynum']})
    ]


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    def gender(self):
        if self.gender:
            return '男'
        else:
            return '女'

    def delete(self):
        if self.isDelete:
            return '是'
        else:
            return '否'

    list_display = ['pk', 'sname', gender, 'sage', 'sintroduction', 'sgrade', delete]
    list_filter = ['sname', 'sage', 'sgrade']  # 过滤器
    search_fields = ['sname', 'sage', 'sgrade']  # 搜索栏
    list_per_page = 4  # 分页
    fieldsets = [
        ('base', {'fields': ['sname', 'sgender', 'sage']}),
        ('other', {'fields': ['sintroduction', 'sgrade', 'isDelete']})
    ]
