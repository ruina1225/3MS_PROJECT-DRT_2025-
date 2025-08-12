import requests
import json
import random

API_URL = "http://localhost:1122/routes/add"

def generate_incheon_latlng():
    lat = round(random.uniform(37.33, 37.58), 6)
    lng = round(random.uniform(126.60, 126.80), 6)
    return {"lat": lat, "lng": lng}

def generate_dummy_route():
    path = [generate_incheon_latlng() for _ in range(random.randint(3, 7))]
    route_latlng = json.dumps(path)
    return route_latlng

def post_dummy_route():
    route_latlng = generate_dummy_route()
    data = {
        "optimal_path_json": route_latlng
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        print(f"등록 성공")
    else:
        print(f"등록 실패: status={response.status_code}, detail={response.text}")

if __name__ == "__main__":
    for _ in range(10):  # 10개 데이터 생성 및 전송
        post_dummy_route()
