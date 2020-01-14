#파일명 : bs01.py #########################
from bs4 import BeautifulSoup

with open('./resources/exam1.html', encoding = 'utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    # div태그 전체 찾기
    all_divs = soup.find_all("div")
    soup.find_all("div", {"class":"first"})
    #print(all_divs) # <div class="first" id="id"> list

    # div태그 첫번째 찾기
    first_div = soup.find("div")
    print(first_div) # <div class="first" id="id"> 

    # print(all_div)    
    for tmp in all_divs:
        print(tmp)
        all_p = tmp.find_all("p")
        print(all_p) # list 모양 => 반복문
        for tmp1 in all_p:
            print(tmp1.text)

    

