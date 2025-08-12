import random
import requests
from faker import Faker

fake = Faker('ko_KR')

class VisitDummyGeneratorSimple:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.users = []
        self.hospitals = []
        # self.routes = []  # 더 이상 사용 안 함
        self.load_users()
        self.load_hospitals()
        # self.load_routes()  # 호출 삭제

    def load_users(self):
        resp = requests.get(f"{self.api_base_url}/users")
        if resp.status_code == 200:
            data = resp.json()
            # 만약 data가 dict이고, key가 "users"이면 users 리스트를 꺼내서 저장
            if isinstance(data, dict) and "users" in data:
                self.users = data["users"]
            else:
                self.users = data
            print(f"Loaded {len(self.users)} users")
        else:
            raise Exception(f"Failed to load users: {resp.text}")

    def load_hospitals(self):
        resp = requests.get(f"{self.api_base_url}/hospitals")
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "hospitals" in data:
                self.hospitals = data["hospitals"]
            else:
                self.hospitals = data
            print(f"Loaded {len(self.hospitals)} hospitals")
        else:
            raise Exception(f"Failed to load hospitals: {resp.text}")


    @staticmethod
    def generate_incheon_lat_lng():
        lat = random.uniform(37.3, 37.6)
        lng = random.uniform(126.6, 127.1)
        return round(lat, 6), round(lng, 6)

    def generate_visit_data(self):
        user = random.choice(self.users)
        hospital = random.choice(self.hospitals)
        route_id = 1  # 임의 고정 route_id 지정

        visit_time = fake.date_time_between(start_date='-1y', end_date='now')

        pickup_lat, pickup_lng = self.generate_incheon_lat_lng()
        dropoff_lat, dropoff_lng = self.generate_incheon_lat_lng()

        visit_payload = {
            "user_id": user['user_id'],
            "hospital_id": hospital['hospital_id'],
            "visit_time": visit_time.isoformat(),
            "pickup_lat": pickup_lat,
            "pickup_lng": pickup_lng,
            "dropoff_lat": dropoff_lat,
            "dropoff_lng": dropoff_lng,
            "route_id": route_id
        }

        resp = requests.post(f"{self.api_base_url}/visits/add", json=visit_payload)
        if resp.status_code == 201:
            print(f"Visit added: user_id={user['user_id']}, hospital_id={hospital['hospital_id']}, route_id={route_id}")
            return True
        else:
            print(f"Failed to add visit: {resp.text}")
            return False

    def generate_bulk_visits(self, count=100):
        success = 0
        for _ in range(count):
            if self.generate_visit_data():
                success += 1
        print(f"Generated {success}/{count} visits successfully.")

if __name__ == "__main__":
    API_BASE_URL = "http://localhost:1122"
    generator = VisitDummyGeneratorSimple(API_BASE_URL)
    generator.generate_bulk_visits(50)
