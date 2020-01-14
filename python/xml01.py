from xml.etree.ElementTree import parse

doc = parse('./resources/exam1.xml')

a = doc.findall("student")
print(a)

for tmp in a :
    # print(tmp)
    print(tmp.findtext("name")) #<name>a</name>
    print(tmp.findtext("age")) #<age>12</age>
    print(tmp.find("addr").attrib) #<addr id="a">addr1</addr>
    #{"id":"a"}