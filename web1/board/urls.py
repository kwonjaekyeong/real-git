
# 파일명 : board/ursl.py
from django.urls import path
from. import views

urlpatterns = [
    path('write', views.write, name="write"),
    path('list', views.list, name="list"),
    path('content', views.content, name="content"),
]