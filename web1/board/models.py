from django.db import models

class Table1(models.Model): # 장고에 있는 모델을 상속!
    object = models.Manager() # vs code 오류 제거용

    no      = models.AutoField(primary_key=True) 
    title   = models.CharField(max_length=200)
    content = models.TextField()
    writer  = models.CharField(max_length=50)
    hit     = models.IntegerField()
    img     = models.BinaryField(null=True) # 바이너리 필드
    regdate = models.DateTimeField(auto_now_add=True)


class Table2(models.Model):
    objects = models.Manager() # vs코드 오류제거용

    no      = models.AutoField(primary_key=True) 
    name    = models.CharField(max_length=30)
    kor     = models.IntegerField()
    eng     = models.IntegerField()
    math    = models.IntegerField()
    regdate = models.DateTimeField(auto_now_add=True)


class Table3(models.Model):
    objects = models.Manager() # vs코드 오류제거용

    no      = models.AutoField(primary_key=True) 
    name    = models.CharField(max_length=30)
    hei     = models.IntegerField()
    wei     = models.IntegerField()