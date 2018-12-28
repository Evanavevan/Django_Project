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

    @classmethod
    def creatstu(cls, name, gender, age, introduction, isDelete, grade):
        s = cls(sname=name, sgender=gender, sage=age, sintroduction = introduction, isDelete=isDelete, sgrade=grade)
        return s

from tinymce.models import HTMLField
# 富文本
class Text(models.Model):
    string = HTMLField()
