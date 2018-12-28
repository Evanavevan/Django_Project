from django.db import models

# Create your models here.


class Grades(models.Model):
    gname = models.CharField(max_length=20)
    gdate = models.DateField()
    ggirlnum = models.IntegerField()
    gboynum = models.IntegerField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.gname


class Students(models.Model):
    sname = models.CharField(max_length=20)
    sgender = models.BooleanField(default=True)
    sage = models.IntegerField()
    sintroduction = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    sgrade = models.ForeignKey('Grades')

    def __str__(self):
        return '%s' % self.sname

    # 在模型类中增加一个类方法
    @classmethod
    def createstudent(cls, name, gender, age, introduction, grade, isDel=False):
        stu = cls(sname=name, sgender=gender, sage=age, sintroduction=introduction, sgrade=grade)
        return stu


# 自定义管理器Manager类
class StudentsManager(models.Manager):
    def get_queryset(self):
        return super(StudentsManager, self).get_queryset().filter(isDelete=False)