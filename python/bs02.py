from bs4 import BeautifulSoup
import requests
    
"""
<div class="tit3">
	<a href="/movie/bi/mi/basic.nhn?code=135874" title="스파이더맨: 홈커밍">스파이더맨: 홈커밍</a>
	</div>
"""

url = "http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20170714"
str = requests.get(url)
# print(str.text)

soup = BeautifulSoup(str.text, 'html.parser')

all_div_tit3 = soup.find_all('div', {"class":"tit3"})
for tmp in all_div_tit3:
    # <a href="#", id="aaa">가나다</a>
    # print(tmp) -> div 내에 있는 모든 내용 출력
    print(tmp.find("a").text) # 텍스트만 출력 ex) 가나다
    print(tmp.find("a").attrs) # {'href':'#','id':'aaa'}


