from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        # 에코프로비엠 종목코드 (네이버 금융 표준)
        code = "247540" 
        url = f"https://finance.naver.com/item/main.naver?code={code}"
        
        # 네이버 서버가 로봇으로 오해해서 차단하는 것을 막기 위한 브라우저 흉내 내기 방패
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        # 네이버 금융 페이지 가져오기
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 금융 HTML 구조에서 현재가(today) 영역을 찾아 숫자만 추출합니다.
        today_div = soup.find('div', class_='today')
        if today_div:
            blind_span = today_div.find('span', class_='blind')
            if blind_span:
                current_price = blind_span.text.strip()
                return current_price # 예: "247,500" 형태로 바로 리턴
                
        return "가격을 찾을 수 없음"
            
    except Exception as e:
        return f"에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
