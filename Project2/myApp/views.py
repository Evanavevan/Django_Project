from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('evan is a handsome and good man!')


#GET属性演示案例
def get1(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    return HttpResponse('a = ' + a + '\nb = ' + b + '\nc = ' + c)

def get2(request):
    a = request.GET.getlist('a')
    c = request.GET.get('c')
    return HttpResponse('a = ' + a[0] + '\nb = ' + a[1] + '\nc = ' + c)


from .models import Grades, Students
#POST属性演示
def registerpage(requset):
    return render(requset, 'myApp/register.html')

def register(request):
    name = request.POST.get('name')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    introduction = request.POST.get('introduction')
    grade = request.POST.get('grade')

    stu = Students()
    grade1 = Grades.objects.get(pk=1)
    grade2 = Grades.objects.get(pk=2)
    grade3 = Grades.objects.get(pk=3)
    grade4 = Grades.objects.get(pk=4)

    stu.sname = name
    stu.sgender = gender
    stu.sage =age
    stu.sintroduction = introduction
    if grade == '1':
        stu.sgrade = grade1
    elif grade == '2':
        stu.sgrade = grade2
    elif grade == '3':
        stu.sgrade = grade3
    else:
        stu.sgrade = grade4
    stu.save()

    studentList = Students.objects.all()
    return render(request, 'myApp/students.html', {'students':studentList})
#    return HttpResponse('Successful!')
#    return redirect(registerpage)



def students(request):
    studentList = Students.objects.all()
    return render(request, 'myApp/students.html', {'students':studentList})


def return_(requset):
    return redirect(registerpage)


from django.contrib.auth import logout
#回话保存信息演示
def mainpage(request):
    username = request.session.get('username', '游客')
    return render(request, 'myApp/mainpage.html', {'username':username})

def login(request):
    return render(request, 'myApp/login.html')

def showmainpage(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    #存储session
    request.session['username'] = username
    request.session['password'] = password
    return redirect('/mainpage')

def logout_(request):
    logout(request)     #问题得到了解决，原因就是logout与函数名重合
#    request.session.clear()
#    request.session.flush()
    return redirect('/mainpage')