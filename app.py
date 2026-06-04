from flask import Flask
import requests
import time

app = Flask(__name__)

# 1. 한국거래소(KRX) 정규장 가격 통로
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

# 2. 🚀 [수정] 넥스트레이드(NXT) 대체거래소 가격 통로
@app.route('/price/nxt')
def get_nxt_price():
    try:
        code = "247540" 
        timestamp = int(time.time() * 1000)
        url = f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{code}&_={timestamp}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        areas = data.get('result', {}).get('areas', [])
        
        # 💡 Render 로그 확인용 프린트 (데이터가 제대로 들어오는지 확인)
        print(f"=== 수신된 데이터 Areas 개수: {len(areas)} ===")
        
        # 네이버가 한 통로에 KRX(정규장)와 ATS(넥스트레이드) 데이터를 모두 넣어주므로, 
        # 보통 두 번째 영역(areas[1])에 넥스트레이드 시세가 들어있습니다.
        if len(areas) > 1:
            nxt_datas = areas[1].get('datas', [])
            if nxt_datas:
                current_price = nxt_datas[0]['nv']  # NXT 현재가
                prev_close = nxt_datas[0]['pcv']     # NXT 전일 종가
                change_rate = nxt_datas[0]['cr']     # NXT 등락률
                
                price_str = f"{current_price:,}원"
                if current_price > prev_close:
                    rate_str = f"(+{abs(change_rate):.2f}%)"
                elif current_price < prev_close:
                    rate_str = f"(-{abs(change_rate):.2f}%)"
                else:
                    rate_str = "(0.00%)"
                    
                return f"{price_str} {rate_str}"
                
        # 만약 데이터 영역이 1개뿐이라면 구조 파악을 위해 전체 데이터를 로그에 찍습니다.
        print("상세 데이터 구조:", data)
        return "NXT 데이터를 찾을 수 없음 (정상 운영 시간 외)"
        
    except Exception as e:
        return f"NXT 에러: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
