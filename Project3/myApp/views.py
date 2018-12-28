from django.shortcuts import render, redirect
from .models import Students

# Create your views here.
def index(request):
    return render(request, 'myApp/index.html')


def verifycodeinput(request):
    return render(request, 'myApp/verifycode.html')


def checkcode(request):
    code1 = request.POST.get('code').lower()
    code2 = request.session['verifycode'].lower()
    if code1 == code2:
        return render(request, 'myApp/success.html')
    else:
        return redirect('/verifycodeinput/')


# 验证反向解析
def student(request):
    studentList = Students.objects.all()
    return render(request, 'myApp/students.html', {'students': studentList})


def retu(request, id):
    return render(request, 'myApp/return.html')


# 模板继承
def main(request):
    return render(request, 'myApp/main.html')