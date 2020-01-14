# 파일명 : flask01.py 

from flask import Flask, render_template, request, redirect

import cx_Oracle as oci # pip conda install cx_oracle

# 아이디/ 암호@서버주소:포트번호/SID
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
cursor = conn.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    sql = "SELECT * FROM MEMBER"
    cursor.execute(sql)
    data = cursor.fetchall() 
    return render_template('list.html', list=data)
    # 나이의 합은 어떻게 구할까? [(azcㅇe), (), (), (), (), ()]
    print(type(data))
    print(data)
    
    sum=0
    for i in data :
        a,b,c,d,e = i
        sum += d
    print(sum)
    return "index page"


@app.route("/join", methods=['GET'])
def join():
    return render_template('join.html')

@app.route("/join", methods=['POST'])
def join_post():
    a = request.form['id']
    b = request.form['pw']
    c = request.form['name']
    d = request.form['age']

    # DB에 값을 넣고 
    # print("{}:{}:{}:{}".format(a,b,c,d))
    # 리턴 전까지 우리가 해야할일!
    sql =  "INSERT INTO MEMBER VALUES(:id, :pw, :na, :ag, SYSDATE)"
    cursor.execute(sql, id=a, pw=b, na=c, ag=d)
    conn.commit()
    



    # 오라클 DB접속
    # 추가하는 SQL문 작성 -=> INSERT, SELECT, UPDATE, DELETE
    # SQL문 수행
    
    return redirect('/') # 127.0.0.1/  크롬에서 입력한 것 처럼 동작
    

# 내가 한 것!
@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login_post():
    print("login-posts")


if __name__=='__main__':
    app.run(debug=True)  






    