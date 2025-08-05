from fastapi import APIRouter, HTTPException
from app.database import get_db_conn

router = APIRouter()

# 1. visitor 조회
@router.get("/")
async def get_all_visits():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                visit_id, user_id, hospital_id, 
                TO_CHAR(visit_time, 'YYYY-MM-DD HH24:MI:SS'),
                origin_lat, origin_lng, 
                dest_lat, dest_lng, route_id
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
                "origin_lat": row[4],
                "origin_lng": row[5],
                "dest_lat": row[6],
                "dest_lng": row[7],
                "route_id": row[8]
            }
            for row in rows
        ]

        return result

    except Exception as e:
        print("에러:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# user_id별 사용자 조회
@router.get("/visits/user/{user_id}")
async def get_visits_by_user(user_id: int):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                visit_id, user_id, hospital_id, 
                TO_CHAR(visit_time, 'YYYY-MM-DD HH24:MI:SS') AS visit_time,
                origin_lat, origin_lng, 
                dest_lat, dest_lng, route_id
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
                "origin_lat": row[4],
                "origin_lng": row[5],
                "dest_lat": row[6],
                "dest_lng": row[7],
                "route_id": row[8]
            }
            for row in rows
        ]

        return result

    except Exception as e:
        print("에러:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
