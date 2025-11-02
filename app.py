# app.py  — API mock để test app di động ngay
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Cho phép gọi từ web/app (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # khi triển khai thật, có thể siết domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Schema đầu vào -------------------
class PatientData(BaseModel):
    age: float
    BMI: float
    sex: str
    dm: int
    htn: int
    dyslipidemia: int
    pain: int
    shock: int
    resp_fail: int
    GCS: float
    HR: float
    SBP: float
    DBP: float
    RR: float
    Temp: float
    SpO2: float
    triglyceride: float
    amylase: float
    lipase: float
    CRP: float
    lactate: float
    creatinine: float
    AST: float
    ALT: float
    bilirubin: float
    albumin: float
    Na: float
    K: float
    Cl: float
    Ca: float
    Hct: float
    WBC: float
    Plt: float
    INR: float
    CT_done: int
    CTSI: float

# ------------------- Endpoint dự báo (MOCK) -------------------
@app.post("/predict")
def predict(data: PatientData):
    # Công thức giả lập để bạn test luồng từ app (tạm thời chưa dùng mô hình thật)
    # Tính nguy cơ xấp xỉ theo tuổi/BMI + vài ngưỡng đơn giản
    p = 0.05
    p += max(0, (data.age - 40)) / 200.0
    p += max(0, (data.BMI - 18)) / 120.0
    if data.SBP < 90 or data.shock == 1:
        p += 0.20
    if data.SpO2 < 92 or data.resp_fail == 1:
        p += 0.15
    if data.CRP >= 150:
        p += 0.10
    if data.creatinine >= 1.5:
        p += 0.10
    if data.CTSI >= 4:
        p += 0.10

    p = max(0.0, min(1.0, p))
    if p >= 0.40:
        group = "Cao"
    elif p >= 0.15:
        group = "Vừa"
    else:
        group = "Thấp"

    return {"risk_proba": round(p, 4), "risk_group": group, "model_version": "mock-1.0"}
