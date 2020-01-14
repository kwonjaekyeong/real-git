from bs4 import BeautifulSoup
import requests	
    
"""
    <div class="head_info point_dn">
		<span class="value">1.2993</span>
	    <span class="txt_usd"><span class="blind">달러</span></span>
		<span class="change"> 0.0070</span>
		<span class="blind">하락</span>
	</div>

"""

url = "https://finance.naver.com/marketindex/"
str = requests.get(url)
print(str.text)

soup = BeautifulSoup(str.text, 'html.parser')

all_div_head_info= soup.find_all('div', {"class":"head_info point_dn"}) # 변수는 띄어쓰기 할 수 없음!
for tmp in all_div_head_info:
    # print(tmp) #-> div 내에 있는 모든 내용 출력
    
    # <div class="head_info point_dn">
    # <span class="value">1,052.51</span>
    # <span class="txt_krw"><span class="blind">원</span></span>
    # <span class="change"> 0.07</span>
    # <span class="blind">하락</span>
    # </div>

    print(tmp.find("span").text) # 텍스트만 출력