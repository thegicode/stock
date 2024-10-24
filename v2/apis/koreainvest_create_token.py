
import os
import sys
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.get_key import CLIENT_KEY, CLIENT_SECRET


def create_token():
    # 토큰 발급 요청
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": CLIENT_KEY,
        "appsecret": CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, json=body)
    access_token = response.json().get("access_token")
    return access_token

if __name__ == "__main__":
    access_token = create_token()
    print("Access Token:", access_token)
