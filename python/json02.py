import requests
import json
import cx_Oracle as oci
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
cursor = conn.cursor()
"""
{
    'ret':{'id': 'a386', 'name': '123', 'age': 34},
    'ret1':{'id': 'a383', 'name': '123', 'age': 36}
}
"""

url = "http://ihongss.com/json/exam2.json"
str1 = requests.get(url).text
data1 = json.loads(str1) # 타입바꾸는 것!!( # str => dict)

ret = data1['ret']
ret1 = data1['ret1']

sql = """
      INSERT INTO MEMBER(ID, PW, NAME, AGE, JOINDATE)
      VALUES(:ID, 333, :NAME, :AGE, SYSDATE)
      """
cursor.execute(sql, ret)

sql = """
      INSERT INTO MEMBER(ID, PW, NAME, AGE, JOINDATE)
      VALUES(:ID, 333, :NAME, :AGE, SYSDATE)
      """

cursor.execute(sql, ret1)
conn.commit()