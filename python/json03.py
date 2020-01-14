import requests
import json
import cx_Oracle as oci
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
cursor = conn.cursor()


url = "http://ihongss.com/json/exam3.json"
str1 = requests.get(url).text
data1 = json.loads(str1)

# data1 => {ret :[{},{},{}]}, {ret1 :[{},{},{}]}
ret = data1['ret'] # [{},{},{},{}] => [A, B, C, D]
for tmp in ret: #  4번 수행
    print(tmp) # {'id': 'a2001', 'name': '123', 'age': 34}
    sql = """
       INSERT INTO MEMBER(ID, PW, NAME, AGE, JOINDATE)
       VALUES(:id, '333', :name, :age, SYSDATE)
       """   
    cursor.execute(sql, tmp)
conn.commit()