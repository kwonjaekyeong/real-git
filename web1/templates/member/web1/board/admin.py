from django.contrib import admin

# Register your models here.

from board.models import Table1
admin.site.register(Table1)

# conda list => django 버전 확인
# pip install django==2.2.5 => 버전변경
# python manage.py createsuperuser
# admin => 아이디
# 1234  
# 1234
# y