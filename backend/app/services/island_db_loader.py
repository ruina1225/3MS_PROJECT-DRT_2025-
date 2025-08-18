# python -m app.services.island_db_loader
import csv
import os
from app.utils.safe_converter import safe_float
from app.database import get_db_conn

# -----------------------------
# 1️⃣ 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
ISLAND_DATA_DIR = os.path.join(UPLOAD_DIR, "island_data")
INPUT_CSV = os.path.join(ISLAND_DATA_DIR, "islands_latlng.csv")

# -----------------------------
# 2️⃣ CSV 읽기 함수 (인코딩 자동)
def read_csv(file_path):
    encodings = ["utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            with open(file_path, newline="", encoding=enc) as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                print(f"✅ CSV 읽기 성공: {file_path} ({enc})")
                return rows
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"CSV 파일 인코딩을 읽을 수 없습니다: {file_path}")

# -----------------------------
# 3️⃣ DB 삽입 함수
def insert_islands_to_db(rows):
    conn = get_db_conn()
    cursor = conn.cursor()
    inserted_count = 0

    for row in rows:
        name = row.get("island_name", "").strip()
        lat = safe_float(row.get("latitude"))
        lon = safe_float(row.get("longitude"))

        if not name or lat is None or lon is None:
            print(f"⚠️ 생략: {name} (위경도 없음)")
            continue

        # 중복 체크 (island_name 기준)
        cursor.execute(
            "SELECT COUNT(*) FROM ISLANDS_DRT WHERE island_name = :1",
            (name,)
        )
        if cursor.fetchone()[0] > 0:
            print(f"⏩ 이미 존재: {name}")
            continue

        try:
            cursor.execute(
                """
                INSERT INTO ISLANDS_DRT
                (island_name, latitude, longitude)
                VALUES (:1, :2, :3)
                """,
                (name, lat, lon)
            )
            inserted_count += 1
            print(f"📍 저장: {name} → 위도: {lat}, 경도: {lon}")
        except Exception as e:
            print(f"❌ DB 오류: {name} → {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ DB 저장 완료! 총 삽입: {inserted_count}개")

# -----------------------------
# 4️⃣ 메인 실행
if __name__ == "__main__":
    rows = read_csv(INPUT_CSV)
    insert_islands_to_db(rows)