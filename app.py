from flask import Flask
import requests
import time

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        code = "247540" # 에코프로비엠
        
        # ⏱️ 요청할 때마다 매번 다른 '현재 시간 숫자'를 생성합니다. (네이버 캐시 무력화 용도)
        timestamp = int(time.time() * 1000)
        
        # 네이버 금융의 내부 실시간 데이터 통로 주소입니다.
        url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}&_={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        # 데이터를 가져와서 텍스트가 아닌 JSON(딕셔너리 구조)으로 바로 변환합니다.
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # 네이버 실시간 데이터 구조 안에서 현재가(nv = Now Value)만 쏙 빼옵니다.
        datas = data['result']['areas'][0]['datas']
        if datas:
            current_price = datas[0]['nv'] # 현재 주가 (숫자 형태)
            return f"{current_price:,}"    # 쉼표를 붙여서 출력 (예: 247,500)
            
        return "가격을 찾을 수 없음"
            
    except Exception as e:
        return f"에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
