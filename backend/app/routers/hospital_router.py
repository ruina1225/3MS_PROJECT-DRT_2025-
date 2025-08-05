from fastapi import APIRouter, HTTPException
from app.database import get_db_conn

router = APIRouter()

# 1. 모든 병원 조회
@router.get("/")
async def get_hospitals():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hospital_id, name, latitude, longitude, hospital_type, phone, room_count, bed_count FROM hospitals_drt
        """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "hospitals": [
            {
               "hospital_id" : row[0],
               "name" : row[1],
               "latitude" : row[2],
               "longitude" : row[3],
               "hospital_type" : row[4],
               "phone" : row[5],
               "room_count" : row[6],
               "bed_count" : row[7]
            } for row in rows
        ]
    }

# 2. 병원별 부서 조회
@router.get("/hospital_dept/{hospital_id}")
async def get_hospital_dept(hospital_id: int):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT dept_id, hospital_id, dept_name 
            FROM hospital_depts_drt  
            WHERE hospital_id = :id
        """, {"id": hospital_id})
        
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not rows:
            raise HTTPException(status_code=404, detail="hospital department not found")
        
        return [
            {
                "dept_id": row[0],
                "hospital_id": row[1],
                "dept_name": row[2]
            }
            for row in rows
        ]
    
    except Exception as e:
        print("에러:", e)  # 콘솔에 에러 출력
        raise HTTPException(status_code=500, detail="Internal Server Error")
