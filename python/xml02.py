from xml.etree.ElementTree import parse
# import requests
from urllib.request import urlopen

url = 'http://ihongss.com/xml/exam1.xml'
# str = requests.get(url)
# doc = parse(str.text)
# print(doc)

str1 = urlopen(url)
doc1 = parse(str1)
print(doc1)

for item in doc1.iterfind('items/item'):
    print(item.attrib) #<item id="a">
    print(item.findtext("name")) #<name>a</name>
