from django.shortcuts import render
from django.http import HttpResponse


from .models import Item
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json

# 127.0.0.1:8000/api/select1?key=abc&no=5
#{"id":"a"} => 물품 1개
def select1(request):
    key = request.GET.get("key", "")
    no = request.GET.get("no", "1")
    search = request.GET.get("search","")
    #DB 에서 확인
    
    data = json.dumps({"ret":'key error'})

    if (key == "abc") and (no=='13') and (search=='휴'):
        
        #obj = Item.objects.get(no=no)

        # SELECT * FROM MT2 WHERE name LIKE '%가%'
        list = Item.objects.filter(name__contains='휴')[0:3]
        
        serializer = ItemSerializer(list, many=True)
        data = JSONRenderer().render(serializer.data)
    
    return HttpResponse(data)


#{"id":"a"}, {"id":"b"} => 물품 여러개 
def select2(request):
    for i in range(1,31,1):
        obj =  Item.objects.all()
        obj.name = '피자'+str(i)
        obj.price = 1000+i
    

    return HttpResponse("insert1")


def insert1(request):
    for i in range(1,31,1):
        obj =  Item()
        obj.name = '피자'+str(i)
        obj.price = 1000+i
        obj.save()

    return HttpResponse("insert1")


