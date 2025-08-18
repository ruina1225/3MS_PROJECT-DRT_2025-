from fastapi import APIRouter
from app.database import get_db_conn # 기존 커넥션
import os

router = APIRouter()

# user_router.py 파일 위치 기준 절대경로 구하기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # user_router.py가 있는 폴더

# # 프로젝트 기준 uploads 폴더 (user_router.py 기준 1단계 위로 올라가서 uploads 폴더 지정)
# UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads")         # backend/app/uploads
# UUID_IMG_DIR = os.path.join(UPLOAD_DIR, "uuid_img")

# os.makedirs(UUID_IMG_DIR, exist_ok=True)

# 1. 모든 섬 조회
@router.get("/")
async def get_users():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT island_id,island_name,latitude,longitude FROM islands_drt ORDER BY island_id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "users": [
            {
                "island_id": row[0],
                "island_name": row[1],
                "latitude": row[2],
                "longitude": row[3],
            } for row in rows
        ]
    }