from flask import Flask
import yfinance as yf

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        ticker_symbol = "247540.KQ" # 에코프로비엠
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d", interval="1m")
        
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            return f"{int(current_price):,}"
        else:
            return "시장 닫힘"
            
    except Exception as e:
        return f"에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)