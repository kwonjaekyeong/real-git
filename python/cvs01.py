import csv
import pymongo

#http://ihongss.com/csv/exam1.csv

conn = pymongo.MongoClient('192.168.99.100', 32766)
 

db = conn.get_database("db1")
coll = db.get_collection("exam1")

f = open('./resources/exam1.csv', 'r', encoding="utf-8")
rdr = csv.reader(f)
next(rdr, None) # 컬럼 skip
for line in rdr:
    print(type(line))
    print(line)
    dict1 = dict()
    dict1[line[0]] = line
    coll.insert_one(dict1)

conn.close()
