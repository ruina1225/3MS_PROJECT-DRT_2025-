# python -m app.services.hospital_db_loader
import csv
from app.utils.safe_converter import safe_int, safe_float
from app.database import get_db_conn
import os

# 현재 파일의 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 프로젝트 루트(app 폴더 기준)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
HOSPITAL_DATA_DIR = os.path.join(UPLOAD_DIR, "hospital_data")

# 지오코딩된 CSV 경로 지정
input_path = os.path.join(HOSPITAL_DATA_DIR, "hospitals_geocoded_final.csv")

# Oracle 연결 정보
conn = get_db_conn()
cursor = conn.cursor()

with open(input_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get("name", "").strip()
        addr = row.get("address", "").strip()
        type_ = row.get("hospital_type", "").strip()
        phone = row.get("phone", "").strip()
        room = safe_int(row.get("room_count", 0))
        bed = safe_int(row.get("bed_count", 0))
        lat = safe_float(row.get("latitude"))
        lon = safe_float(row.get("longitude"))

        if lat is not None and lon is not None:
            print(f"📍 저장: {name}, {addr} → 위도: {lat}, 경도: {lon}")
            cursor.execute("""
                INSERT INTO HOSPITALS_DRT
                (name, address, hospital_type, phone, room_count, bed_count, latitude, longitude)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
            """, (name, addr, type_, phone, room, bed, lat, lon))
        else:
            print(f"⚠️ 위경도 없음 → 생략: {name}")

    conn.commit()
    print("✅ DB 저장 완료")

cursor.close()
conn.close()

