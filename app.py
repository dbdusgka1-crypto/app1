from flask import Flask
import requests
from bs4 import BeautifulSoup
import time
import yfinance as yf

app = Flask(__name__)

# 1. [기존 위젯용] 에코프로비엠 통로
@app.route('/price')
def get_price():
    try:
        code = "247540" 
        timestamp = int(time.time() * 1000)
        url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}&_={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        datas = data['result']['areas'][0]['datas']
        if datas:
            current_price = datas[0]['nv'] 
            prev_close = datas[0]['pcv']   
            change_rate = datas[0]['cr']   
            
            price_str = f"{current_price:,}원"
            if current_price > prev_close:
                rate_str = f"(+{abs(change_rate):.2f}%)"
            elif current_price < prev_close:
                rate_str = f"(-{abs(change_rate):.2f}%)"
            else:
                rate_str = "(0.00%)"
                
            return f"{price_str} {rate_str}"
        return "가격을 찾을 수 없음"
    except Exception as e:
        return f"에러: {str(e)}"

# 2. [새 위젯용] 미국 주식 또는 코인 NXT 통로
@app.route('/price/nxt')
def get_nxt_price():
    try:
        # 🔍 기본 설정은 미국 주식 "NXT" 입니다.
        # 만약 주식이 아니라 코인 가상화폐 가격을 원하시면 "NXT-USD"로 변경해 주세요!
        ticker_symbol = "NXT" 
        ticker = yf.Ticker(ticker_symbol)
        
        # 실시간성이 높은 1일치 분봉 데이터 추출
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            
            # 전일 종가 기준으로 등락률 계산
            prev_close = ticker.info.get('previousClose', current_price)
            change_rate = ((current_price - prev_close) / prev_close) * 100
            
            price_str = f"${current_price:,.2f}" # 달러 표기 (예: $146.47)
            if change_rate > 0:
                rate_str = f"(+{change_rate:.2f}%)"
            elif change_rate < 0:
                rate_str = f"(-{abs(change_rate):.2f}%)"
            else:
                rate_str = "(0.00%)"
                
            return f"{price_str} {rate_str}"
        return "시장 닫힘 또는 데이터 없음"
    except Exception as e:
        return f"에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
