from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

#定义视图
def index(request):
    return HttpResponse('evan is a handsome and great man!')

def detail(request, num):
    return HttpResponse('detail-{}'.format(num))


from .models import Grades, Students
def grades(request):
    #去模板里取数据
    gradeList = Grades.objects.all()
    #将数据传递给模板，模板渲染页面，其后返回给浏览器
    return render(request, 'MyApp/grades.html', {'grades':gradeList})

def students(request):
    #去模板里取数据
    studentsList = Students.objects.all()
    #将数据传递给模板，模板渲染页面，其后返回给浏览器
    return render(request, 'MyApp/students.html', {'students':studentsList})

def gradeStudents(request, num):
    grade = Grades.objects.get(pk=num)
    studentsList = grade.students_set.all()
    return render(request, 'MyApp/students.html', {'students':studentsList})




def addstudent(request):
    grade = Grades.objects.get(pk=2)
    stu = Students.createstudent('刘德华', True, 40, '我是华仔，你们说我帅不帅', grade)
    stu.save()
    return HttpResponse('Successful!')
