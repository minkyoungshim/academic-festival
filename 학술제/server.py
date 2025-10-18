from flask import Flask, request, jsonify, redirect
import requests
from urllib.parse import urlencode
import base64

app = Flask(__name__)

# Fitbit 앱 설정
client_id = '23PVVC'
client_secret = '1dfd56b33e39c24f5d9c8b567b044409'
redirect_uri = 'https://mingk203.github.io/fitcoin/callback.html'  # HTML 페이지와 일치해야 함
scope = 'activity heartrate sleep'

# Fitbit Authorization URL 생성
@app.route('/auth-url')
def auth_url():
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    }
    url = f"https://www.fitbit.com/oauth2/authorize?{urlencode(params)}"
    return redirect(url)

# 인증 코드로 액세스 토큰 요청
@app.route('/callback-auth', methods=['POST'])
def callback_auth():
    auth_code = request.json.get('code')
    token_url = "https://api.fitbit.com/oauth2/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": auth_code
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()

    if 'access_token' in token_info:
        access_token = token_info['access_token']
        return jsonify({"accessToken": access_token})
    else:
        return jsonify({"error": token_info}), 400

if __name__ == '__main__':
    app.run(port=5000)
