from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

cursor = connection.cursor()

# django에서 제공하는 User 모델
from django.contrib.auth.models import User
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1
from django.contrib.auth import authenticate as auth1


from.models import Table2
from django.db.models import Sum, Max, Min, Count, Avg

import pandas as pd

import matplotlib.pyplot as plt
import io # byte로 변환
import base64 # byte를 base64로 변경
from matplotlib import font_manager, rc # 한글 폰트 적용

def graph(request):

    # SELECT SUM("kor") FROM MEMBER_TABLE2   
    sum_kor = Table2.objects.aggregate(Sum("kor"))
    print(sum_kor) #"kor__sum1"

    # SELECT SUM("kor") AS sum1 FROM MEMBER_TABLE2
    sum_kor = Table2.objects.aggregate(sum1=Sum("kor"))
    print(sum_kor) #"sum1"
    
    # SELECT SUM("kor") FROM MEMBER_TABLE2
    # WHERE CLASSROOM=102
    sum_kor = Table2.objects.filter(classroom='102').aggregate(sum1=Sum("kor"))
    print(sum_kor)

    # SELECT SUM("kor") FROM MEMBER_TABLE2
    # WHERE KOR > 100
    # > gt, >= gte, < lt, =< lte
    sum_kor = Table2.objects.filter(kor__gt=10).aggregate(sum1=Sum("kor"))
    print(sum_kor)

    # 반별합계
    # SELECT SUM("kor") sum1, SUM("eng") sum2, SUM("math") sum3
    # FROM MEMBER TABLE2
    # GROUP BY CLASSROOM
    sum_kor = Table2.objects.values("classroom").annotate(sum1=Sum("kor"), sum2=Sum("eng"), sum3=Sum("math"))
    print(sum_kor)
    print(sum_kor.query) #SQL문으로 확인


    df =  pd.DataFrame(sum_kor)
    print(df)
    df.plot(kind="bar")
    x = ['kor', 'eng', 'math']
    y = [ 45, 3, 4]
    
    # 폰트읽기
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()

    
    # 폰트 적용
    rc('font', family=font_name)


    plt.bar(x,y)
    plt.title("AGES & PERSON")
    plt.xlabel("나이")
    plt.ylabel("숫자")

    #plt.show() # 표시
    plt.draw() # 안보이게 그림을 캡쳐
    img =  io.BytesIO() # img에 byte배열로 보관
    plt.savefig(img, format = "png") # png파일 포맷으로 저장
    img_url = base64.b64encode(img.getvalue()).decode()
    
    plt.close() # 그래프 종료

    return render(request, 'member/graph.html', {"graph1":'data:;base64,{}'.format(img_url)})
    # <img src="{{graph1}}"/>  <= graph.html에서 

 



def dataframe(request):
    # SELECT * FROM MEMBER_TABLE2
    # rows = Table2.objects.all()

    # 1. QuerySet -> list로 변경
    # SELECT NO, NAME, KOR FROM MEMBER_TABLE2
    rows = list(Table2.objects.all().values("no", "name", "kor"))[0:10]
    print(rows)

    
    # 2. list -> dataframe 으로 변경
    df =  pd.DataFrame(rows)
    print(df)
    return render(request, "member/dataframe.html", {"df_table": df.to_html(), "list":rows})

    # 3. dataframe -> list
    rows1 = df.values.tolist()


def js_chart(request):
    if request.method == "GET": 
        return render(request, 'member/js_chart.html') 

def js_index(request):
    str = "100, 200, 300, 400, 200, 100"
    return render(request, 'member/js_index.html', {"str":str}) 

def exam_list(request):
    if request.method == "GET": 
        rows =  Table2.objects.all()  
        # SQL : SELECT * FROM BOARD_TABLE2
        print(rows)   #결과확인
        print(type(rows))   #타입확인--> 클래스
        return render(request, 'member/exam_list.html', {"list":rows})   # html표시

@csrf_exempt
def exam_select(request):
    txt = request.GET.get("txt", "")
    page = int(request.GET.get("page", 1))

    if txt == "" : # 검색어가 없는 경우 전체 출력
        # SELECT * FROM MEMBER_TABLE2 
        list = Table2.objects.all()[page*10-10:page*10]
    
        # SELECT COUNT (*) FROM MEMBER_TABLE2
        cnt  = Table2.objects.all().count()
        tot  = (cnt-1)//10+1

    else: # 검색어가 있는 경우
        # SELECT * FROM MTEWHERE name LIKE '%가%'
        list = Table2.objects.filter(name__contains=txt)[page*10-10:page*10]

        # SELECT COUNT(*) FROM MTE WHERE name LIKE '%가%'
        cnt  = Table2.objects.filter(name__contains=txt).count() 
        tot  = (cnt-1)//10+1

    return render(request, 'member/exam_select.html', {"list":list, "pages":range(1,tot+1,1)})
        


@csrf_exempt
def exam_insert(request):
    if request.method == "GET": 
        return render(request, 'member/exam_insert.html')
    elif request.method=='POST':
        obj = Table2() #obj객체 생성
        obj.name = request.POST['name'] #변수에 값
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.save() #저장하기 수행

        return redirect("/member/exam_insert")


@csrf_exempt
def exam_delete(request):
    if request.method == "GET": 
        n = request.GET.get("no",0)
        rows =  Table2.objects.get(no=n)
        rows.delete() 
        return redirect("/member/exam_insert")

@csrf_exempt
def exam_update(request):
    if request.method == "GET": 
        n = request.GET.get("no",0)
        row =  Table2.objects.get(no=n)
        return render(request, "member/exam_update.html", {"one":row}) 
    elif request.method=='POST':
        n = request.POST['no'] 
        obj = Table2.objects.get(no=n) 
        obj.name = request.POST['name'] 
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['classroom']
        obj.save()  
        return redirect("/member/exam_insert")

@csrf_exempt
def exam_update_all(request):
    if request.method == "GET": 
        n = request.session['no'] 
        print(n)
        rows = Table2.objects.filter(no__in=n)
        return render(request, 'member/exam_update_all.html', {"list":rows})
    elif request.method=='POST':
        menu = request.POST['menu']
        if menu == '1' :
            no = request.POST.getlist("chk[]")
            request.session['no'] = no
            print(no)
            return redirect("/member/exam_update_all")
        elif menu == '2' :
            no =  request.POST.getlist("no[]")
            name =  request.POST.getlist("name[]")
            kor =  request.POST.getlist("kor[]")
            eng =  request.POST.getlist("eng[]")
            math =  request.POST.getlist("math[]")
            classroom = request.POST.getlist("classroom[]")
            
            objs = []
            for i in range(0, len(no), 1):
                obj = Table2.objects.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                obj.classroom = classroom[i]
                objs.append(obj)
           
            return redirect("/member/exam_list")



###########################################################
"""
@csrf_exempt
def exam_select(request):
    if request.method == "GET":
        return render(request, 'member/exam_select.html')
    elif request.method =='POST':
        obj = Table2()
        obj.name = request.POST['name']
        obj.kor = request.POST['kor']
        obj.eng = request.POST['eng']
        obj.math = request.POST['math']
        obj.classroom = request.POST['classroom']
        obj.save()
  

        return redirect("/member/exam_select")
"""        
#################################################################


#######################################################################
@csrf_exempt
def auth_login(request):
    if request.method == "GET": 
        return render(request, 'member/auth_login.html')
    elif request.method =='POST':
        id = request.POST['username']
        pw = request.POST['password']
        #DB에 인증
        obj =  auth1(request, username=id, password=pw)
        if obj is not None:
            login1(request, obj)      # 세션에 추가
            return redirect("/member/auth_index")
        return redirect("/member/auth_login")

        
@csrf_exempt
def auth_logout(request):
    if request.method == 'GET' or request.method == 'POST':
        logout1(request)  # 세션 초기화
        return redirect('/member/auth_index')

@csrf_exempt
def auth_pw(request):
    if request.method == 'GET' :
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")
        
        return render(request,'member/auth_pw.html')

    elif request.method == 'POST':
        pw = request.POST['pw']  # 기존 암호
        pw1 = request.POST['pw1']  # 바꿀 암호
        #바꾸기 전에 인증
        obj = auth1(request, username=request.user, password=pw)
        if obj:
            obj.set_password(pw1) # pw1으로 암호 변경
            obj.save()
            return redirect("/member/auth_index")

        return redirect("/member/auth_pw")


@csrf_exempt
def auth_edit(request):
    if request.method == 'GET' :
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")
        
        obj = User.objects.get(username=request.user)
        return render(request,'member/auth_edit.html', {"obj":obj})
    
    elif request.method == 'POST':
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.get(username=id)
        obj.first_name = na
        obj.email = em
        obj.save()
        return redirect("/member/auth_index")


@csrf_exempt
def auth_join(request):
    if request.method == "GET": 
        return render(request, 'member/auth_join.html')
    elif request.method=='POST':
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        # 회원가입
        obj = User.objects.create_user(
            username=id,
            password=pw,
            first_name=na,
            email=em)
        obj.save()
        return redirect("/member/auth_index")
 

@csrf_exempt
def auth_index(request):
    if request.method == "GET": 
        return render(request, 'member/auth_index.html')


@csrf_exempt
def delete (request):
    if request.method == "GET" or request.method =='POST':
        ar = [request.session['userid']]
        sql = "DELETE FROM MEMBER WHERE ID=%s"
        cursor.execute(sql, ar)

        return redirect("/member/logout")



@csrf_exempt
def edit(request):
    if request.method == "GET":    # 개인정보 불러오기!
        ar = [request.session['userid']]
        sql="""
            SELECT * FROM MEMBER WHERE ID=%s
        """
        cursor.execute(sql, ar)
        data = cursor.fetchone() # fetchone(한사람), fetchalㅣ
        print(data)

        return render(request, 'member/edit.html', {"one":data})
    elif request.method=='POST':
        ar = [
            request.POST['name'],
            request.POST['age'],
            request.POST['id'],
        ]
        sql="""
            UPDATE MEMBER SET NAME=%s, AGE=%s
            WHERE ID=%s
        """
        cursor.execute(sql, ar)

        return redirect("/member/index")


def join1(request):
    if request.method == "GET":    
        return render(request, 'member/join1.html')

def list1(request):
    # ID 기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql) #sql문 실행
    data = cursor.fetchall()  # 결과값을 가져옴
    print(type(data)) # list
    print(data) #[(1,2,3,4,5),(   ),(   )]

    # list.html 을 표시하기 전에
    # list 변수에 data값을, title 변수에 "회원목록"  문자를
    return render(request, 'member/list1.html', 
        {"list":data, "title": "회원목록"}) 


    

def index(request):
    #return HttpResponse("index page <hr/>")
    return render(request, 'member/index.html')


@csrf_exempt #post로 값을 전달 받는 곳은 필수
def login(request): 
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        ar =[request.POST['id'], request.POST['pw']]
        sql = """
            SELECT ID, NAME FROM MEMBER  
            WHERE ID=%s AND PW=%s
            """
        cursor.execute(sql, ar)
        data = cursor.fetchone()
        print(type(data))
        print(data)

        if data:
            request.session['userid']= data[0]  # 키 
            request.session['username']= data[1]
        return redirect('/member/index')

    return redirect('/member/login') # 실패시에는 로그인으로 간다!

@csrf_exempt
def logout(request):
    if request.method=='GET' or request.method=='POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/member/index')

@csrf_exempt #post로 값을 전달 받는 곳은 필수
def join(request):
    if request.method =='GET':
        return render(request, 'member/join.html')
    elif request.method == 'POST':
        id =  request.POST['id'] # html에서 넘어오는 값 받기
        na =  request.POST['name']
        ag =  request.POST['age']
        pw =  request.POST['pw']

        ar =  [id, na, ag, pw] # list로 만듬
        print(ar)

        # DB에 추가함
        sql = """
            INSERT INTO MEMBER(ID, NAME, AGE, PW, JOINDATE)
            VALUES (%s, %s, %s, %s, SYSDATE)
            """
        cursor.execute(sql, ar)

        # 크롬에서 127.0.0.1:8000/member/index 엔터키를 자동화
        return redirect('/member/index') # /중요하다!!