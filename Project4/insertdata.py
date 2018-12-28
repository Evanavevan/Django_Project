from myApp.models import Grades, Students


grade = Grades.objects.get(pk=1)
name = "郭富城"
gender = 1
for i in range(1, 201):
    s = Students.creatstu(name, gender, i, "我叫郭富城，我今年%d岁" %i, 1, grade)
    s.save()