from flask import Flask
import yfinance as yf

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        # 🔍 원하는 종목의 티커(Ticker)를 적어줍니다.
        # 예: Apple은 'AAPL', 삼성전자는 '005930.KS', 특정 ETF 등 모두 가능합니다.
        ticker_symbol = "247540.KQ" 
        
        # 주식 정보 가져오기
        ticker = yf.Ticker(ticker_symbol)
        
        # 가장 최근 거래 데이터 1일치 가져오기
        data = ticker.history(period="1d", interval="1m")
        
        if not data.empty:
            # 가장 마지막에 찍힌 종가(실시간 가격) 가져오기
            current_price = data['Close'].iloc[-1]
            return f"{current_price:,.2f}" # 소수점 둘째 자리까지 표기
        else:
            return "시장 닫힘 또는 데이터 없음"
            
    except Exception as e:
        return f"에러 발생: {str(e)}"

if __name__ == '__main__':
    # 외부(스마트폰)에서 접속할 수 있도록 주소를 0.0.0.0으로 열어줍니다.
    # 포트는 8080 외에 편한 포트를 사용하셔도 됩니다.
    app.run(host='0.0.0.0', port=8080)