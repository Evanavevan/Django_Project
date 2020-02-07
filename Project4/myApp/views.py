from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.http import JsonResponse
import os
from django.conf import settings
from .models import Students
from django.core.paginator import Paginator
from .models import Text


# Create your views here.


def index(request):
    return render(request, 'myApp/index.html')


# 上传文件
def upfile(request):
    return render(request, 'myApp/upfile.html')


def savefile(request):
    if request.method == 'POST':
        f = request.FILES['file']
        # 文件在服务器上的路径
        filepath = os.path.join(settings.MEDIA_ROOT, f.name)
        # 读写文件
        with open(filepath, 'wb') as fp:
            for info in f.chunks():  # 读取大文件用.chunks()分块读取
                fp.write(info)
        return HttpResponse('文件上传成功！')
    else:
        return HttpResponse('抱歉，上传失败，请重新上传！')


# 分页显示
def studentpage(request, pageid):
    allList = Students.objects.all()
    pageList = Paginator(allList, 10)
    # 每页的学生信息
    studentpage = pageList.page(pageid)
    # 分页栏最多显示11页
    max_page = 11
    half_max_page = max_page // 2
    page_start = int(pageid) - half_max_page - 1
    page_end = int(pageid) + half_max_page
    pageList = pageList.page_range
    if int(pageid) >= 6 and page_end <= pageList[-1]:
        pageList = pageList[page_start:page_end]
    elif int(pageid) < 6:
        pageList = pageList[0:11]
    else:
        pageList = pageList[-11:]
    return render(request, 'myApp/students.html', {'students': studentpage, 'pageList': pageList})


# ajax演示
def ajax(request):
    return render(request, 'myApp/ajax.html')


def studentsinfo(request):
    stus = Students.objects.all()
    stuList = []
    for s in stus:
        stuList.append([s.sname, s.sage])
    return JsonResponse({"data": stuList})


# 富文本演示
def edit(request):
    return render(request, 'myApp/edit.html')


def saveedit(request):
    info = request.POST.get('str')
    text = Text()
    text.str = info
    text.save()
    # 能存但显示不了
    tList = Text.objects.all()
    print(tList)
    return render(request, 'myApp/showedit.html', {'text': tList})
