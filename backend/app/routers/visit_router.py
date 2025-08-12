from fastapi import APIRouter, HTTPException
from fastapi import Query
from pydantic import BaseModel, Field
from datetime import datetime
from app.database import get_db_conn

router = APIRouter()

# 1. 전체 방문기록 조회
@router.get("/")
async def get_all_visits():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                visit_id, user_id, hospital_id, 
                TO_CHAR(visit_time, 'YYYY-MM-DD HH24:MI:SS'),
                pickup_lat, pickup_lng, 
                dropoff_lat, dropoff_lng, route_id
            FROM visits_drt
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No visit records found")

        result = [
            {
                "visit_id": row[0],
                "user_id": row[1],
                "hospital_id": row[2],
                "visit_time": row[3],
                "pickup_lat": row[4],
                "pickup_lng": row[5],
                "dropoff_lat": row[6],
                "dropoff_lng": row[7],
                "route_id": row[8]
            }
            for row in rows
        ]

        return result

    except Exception as e:
        print("에러:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# 2. 방문 데이터 생성용 Pydantic 모델
class VisitCreateRequest(BaseModel):
    user_id: int
    hospital_id: int
    visit_time: datetime = Field(default_factory=datetime.now)
    pickup_lat: float = Field(..., ge=37.3, le=37.6)
    pickup_lng: float = Field(..., ge=126.6, le=127.1)
    dropoff_lat: float = Field(..., ge=37.3, le=37.6)
    dropoff_lng: float = Field(..., ge=126.6, le=127.1)
    route_id: int


# 3. 방문 데이터 저장 POST 엔드포인트
@router.post("/add", status_code=201)
async def add_visit(visit: VisitCreateRequest):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO visits_drt
            (user_id, hospital_id, visit_time, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, route_id)
            VALUES (:user_id, :hospital_id, :visit_time, :pickup_lat, :pickup_lng, :dropoff_lat, :dropoff_lng, :route_id)
        """, {
            "user_id": visit.user_id,
            "hospital_id": visit.hospital_id,
            "visit_time": visit.visit_time,
            "pickup_lat": visit.pickup_lat,
            "pickup_lng": visit.pickup_lng,
            "dropoff_lat": visit.dropoff_lat,
            "dropoff_lng": visit.dropoff_lng,
            "route_id": visit.route_id
        })

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Visit added successfully"}

    except Exception as e:
        print("에러:", e)
        raise HTTPException(status_code=400, detail=f"Failed to add visit: {e}")


# 4. user_id별 방문기록 조회
@router.get("/user/{user_id}")
async def get_visits_by_user(user_id: int):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                visit_id, user_id, hospital_id, 
                TO_CHAR(visit_time, 'YYYY-MM-DD HH24:MI:SS') AS visit_time,
                pickup_lat, pickup_lng, 
                dropoff_lat, dropoff_lng, route_id
            FROM visits_drt
            WHERE user_id = :user_id
            ORDER BY visit_time DESC
        """, {"user_id": user_id})

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail=f"No visit records found for user_id {user_id}")

        result = [
            {
                "visit_id": row[0],
                "user_id": row[1],
                "hospital_id": row[2],
                "visit_time": row[3],
                "pickup_lat": row[4],
                "pickup_lng": row[5],
                "dropoff_lat": row[6],
                "dropoff_lng": row[7],
                "route_id": row[8]
            }
            for row in rows
        ]

        return result

    except Exception as e:
        print("에러:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 3. 관리자 페이지에서 예약확인 가능 엔드 포인트

@router.get("/filtered")
async def get_filtered_visits(start_date: str = None, end_date: str = None):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        query = """
            SELECT 
                V.visit_id, V.user_id, U.name AS username, V.hospital_id,
                TO_CHAR(V.visit_time, 'YYYY-MM-DD HH24:MI:SS') AS visit_time,
                V.pickup_lat, V.pickup_lng,
                V.dropoff_lat, V.dropoff_lng,
                V.route_id,
                P.photo_filename
            FROM visits_drt V
            JOIN users_drt U ON V.user_id = U.user_id
            LEFT JOIN user_photos_drt P ON U.user_id = P.user_id
            WHERE (:start_date IS NULL OR V.visit_time >= TO_DATE(:start_date, 'YYYY-MM-DD'))
            AND (:end_date IS NULL OR V.visit_time <= TO_DATE(:end_date, 'YYYY-MM-DD'))
            ORDER BY V.visit_id ASC  -- 등록 순서 오름차순 정렬
        """

        cursor.execute(query, {"start_date": start_date, "end_date": end_date})
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            return []

        result = []
        for row in rows:
            # photo_filename이 None일 수도 있음
            photo_filename = row[10]
            photo_url = f"/uploads/uuid_img/{photo_filename}" if photo_filename else None

            result.append({
                "visit_id": row[0],
                "user_id": row[1],
                "username": row[2],
                "hospital_id": row[3],
                "visit_time": row[4],
                "pickup_lat": row[5],
                "pickup_lng": row[6],
                "dropoff_lat": row[7],
                "dropoff_lng": row[8],
                "route_id": row[9],
                "user_image": photo_url,
            })

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
