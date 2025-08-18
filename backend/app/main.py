# uvicorn app.main:app --host=0.0.0.0 --port=1122 --reload

from fastapi import FastAPI
# from whisper_integration import transcribe_audio
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router, hospital_router, visit_router, route_router, island_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# CORS 설정(React가 별도 서버일 때 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# 라우터 등록
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(hospital_router.router, prefix="/hospitals", tags=["Hospitals"])
app.include_router(visit_router.router, prefix="/visits", tags=["Visits"])
app.include_router(route_router.router, prefix="/routes", tags=["Routes"])
app.include_router(island_router.router, prefix="/islands", tags=["Islands"])