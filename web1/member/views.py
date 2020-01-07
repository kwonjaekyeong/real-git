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

def exam_list(request):
    if request.method == "GET": 
        rows =  Table2.objects.all()  
        # SQL : SELECT * FROM BOARD_TABLE2
        print(rows)   #결과확인
        print(type(rows))   #타입확인--> 클래스
        return render(request, 'member/exam_list.html', {"list":rows})   # html표시

@csrf_exempt
def exam_select(request):
    no = request.GET.get('no',0)
    # SELECT SUM(math) FROM MEMBER_TABLE2 
    # WHERE CLASS_ROOM=101
    list = Table2.objects.aggregate(Sum('math'))

    # SELECT NO, NAME FROM MEMBER_TABLE2
    list = Table2.objects.all().values(['no','name'])

    # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
    list = Table2.objects.all().order_by('name')
    #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

    # 반별 국어, 영어, 수학 합계
    # SELECT SUM(kor), SUM(eng), SUM(math)
    # FROM MEMBER_TABLE2
    # GROUP BY CLASSROOM
    if no == '1':
        list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))    
    return render(request, 'member/exam_select.html',{"list":list})
    

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

def list(request):
    # ID 기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql) #sql문 실행
    data = cursor.fetchall()  # 결과값을 가져옴
    print(type(data)) # list
    print(data) #[(1,2,3,4,5),(   ),(   )]

    # list.html 을 표시하기 전에
    # list 변수에 data값을, title 변수에 "회원목록"  문자를
    return render(request, 'member/list.html', 
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