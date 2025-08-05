import pandas as pd
import os

# 현재 파일의 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 프로젝트 루트(app 폴더 기준)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
HOSPITAL_DATA_DIR = os.path.join(UPLOAD_DIR, "hospital_data")

# 파일 경로 설정
input_path = os.path.join(HOSPITAL_DATA_DIR, "l_c0903a3bc93d414e8f7b84cd33264ee0.csv")
output_path = os.path.join(HOSPITAL_DATA_DIR, "hospitals_geocoded_final.csv")
try:
    # CSV 읽기
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    # 컬럼명 변경 (x → longitude, y → latitude) / 지오코딩에서 x,y로만 저장 가능
    df.rename(columns={"type":"hospital_type", "x": "longitude", "y": "latitude"}, inplace=True)

    # 새 파일로 저장
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("✅ 저장 완료: hospitals_geocoded_final.csv")

except Exception as e : 
    print(f"⚠️ 에러 발생: {e}")
