from flask import Flask
import requests
import time

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        code = "247540" # 에코프로비엠
        timestamp = int(time.time() * 1000)
        url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}&_={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        datas = data['result']['areas'][0]['datas']
        if datas:
            current_price = datas[0]['nv'] # 현재가
            prev_close = datas[0]['pcv']   # 전일 종가
            change_rate = datas[0]['cr']   # 등락률
            
            # 1. 가격 뒤에 '원'을 미리 붙여서 포맷팅합니다 (예: 198,700원)
            price_str = f"{current_price:,}원"
            
            # 2. 전일 종가와 비교해서 상승(+) 또는 하락(-) 부호를 예쁘게 붙여줍니다.
            if current_price > prev_close:
                rate_str = f"(+{abs(change_rate):.2f}%)"
            elif current_price < prev_close:
                rate_str = f"(-{abs(change_rate):.2f}%)"
            else:
                rate_str = "(0.00%)"
                
            # 최종 형태 반환: "198,700원 (+1.50%)"
            return f"{price_str} {rate_str}"
            
        return "가격을 찾을 수 없음"
            
    except Exception as e:
        return f"에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
