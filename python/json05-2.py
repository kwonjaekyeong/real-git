# pip install pymongo
import pymongo
import requests
import json

conn = pymongo.MongoClient('192.168.99.100',32766)
db = conn.get_database("db21") # 없으면 db생성
table = db.get_collection("exam10") # collection 생성

url = "http://ihongss.com/json/exam10.json"
str1 = requests.get(url).text
data1 = json.loads(str1) # str -> dict
# print(data1)

"""
[
    {'ret': 'y', 'data': [
        {'id': 'id1', 'name': '가나다1', 'age': 31, 'score': {'math': 50, 'eng': 90, 'kor': 69}},
        {'id': 'id2', 'name': '가나다2', 'age': 32, 'score': {'math': 90, 'eng': 68, 'kor': 80}}, 
        {'id': 'id3', 'name': '가나다3', 'age': 33, 'score': {'math': 70, 'eng':76, 'kor': 60}}, 
        {'id': 'id4', 'name': '가나다4', 'age': 34, 'score': {'math': 80, 'eng': 79, 'kor': 50}}, 
        {'id': 'id5', 'name': '가나다5', 'age': 35, 'score': {'math': 80, 'eng': 78, 'kor': 90}}]
    }
 ]
 """
# print(data1['ret'])

tmp = data1['data']
"""[
        {'id': 'id1', 'name': '가나다1', 'age': 31, 'score': {'math': 50, 'eng': 90, 'kor': 69}},
        {'id': 'id2', 'name': '가나다2', 'age': 32, 'score': {'math': 90, 'eng': 68, 'kor': 80}}, 
        {'id': 'id3', 'name': '가나다3', 'age': 33, 'score': {'math': 70, 'eng':76, 'kor': 60}}, 
        {'id': 'id4', 'name': '가나다4', 'age': 34, 'score': {'math': 80, 'eng': 79, 'kor': 50}}, 
        {'id': 'id5', 'name': '가나다5', 'age': 35, 'score': {'math': 80, 'eng': 78, 'kor': 90}}
        ]"""


for i in tmp:
    dict1 = dict()
    dict1['ret'] = data1['ret'] 
    dict1['id']= i['id']
    dict1['name'] = i['name']
    dict1['age'] = i['age']
    dict1['eng'] = i['score']['eng']

    table.insert_one(dict1)

conn.close()
