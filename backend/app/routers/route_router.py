from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db_conn
import json

router = APIRouter()

# 1. 전체 경로 조회
@router.get("/")
async def get_all_routes():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                route_id, optimal_path_json
            FROM routes_drt
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No routes found")

        result = [
            {
                "route_id": row[0],
                "optimal_path_json": json.loads(row[1]) if row[1] else None
            }
            for row in rows
        ]

        return result

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 2. 경로 등록용 Pydantic 모델
class RouteCreateRequest(BaseModel):
    optimal_path_json: str  # JSON 문자열

# 3. 경로 등록 POST 엔드포인트
@router.post("/add", status_code=201)
async def create_route(route: RouteCreateRequest):
    try:
        # JSON 유효성 검사
        json.loads(route.optimal_path_json)

        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO routes_drt (optimal_path_json)
            VALUES (:optimal_path_json)
        """, {"optimal_path_json": route.optimal_path_json})

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Route added successfully"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for optimal_path_json")

    except Exception as e:
        if cursor:
            cursor.close()
        if conn:
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))
