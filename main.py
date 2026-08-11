from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from catboost import CatBoostClassifier
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from inference import preprocess_and_predict


app = FastAPI(
    title="AI Credit Risk Demo",
    description="Demo hệ thống đánh giá rủi ro khoản vay bằng XGBoost và CatBoost",
    version="1.0.0"
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
@app.get("/", include_in_schema=False)
def home():
    return FileResponse("templates/index.html")


# ==========================================
# 1. LOAD MODEL MỘT LẦN KHI SERVER KHỞI ĐỘNG
# ==========================================

print("⏳ Đang tải các mô hình AI vào bộ nhớ...")


# XGBoost - SAFE Strategy
preprocessor_safe = joblib.load(
    "classic/models/preprocessor_standard.pkl"
)

model_safe = joblib.load(
    "classic/models/XGBoost_model.pkl"
)

THRESHOLD_SAFE = 0.5541


# CatBoost - SWEEP Strategy
preprocessor_sweep = joblib.load(
    "classic/models/preprocessor_native.pkl"
)

model_sweep = CatBoostClassifier()

model_sweep.load_model(
    "classic/models/CatBoost_model.cbm"
)

THRESHOLD_SWEEP = 0.3453


print("✅ Tải mô hình hoàn tất!")


# ==========================================
# 2. CẤU TRÚC DỮ LIỆU KHÁCH HÀNG
# ==========================================

class CustomerFlow(BaseModel):
    person_age: float
    person_income: float
    person_emp_length: float
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    person_home_ownership: str
    loan_intent: str
    loan_grade: str
    cb_person_default_on_file: str


# ==========================================
# 3. HEALTH CHECK
# ==========================================

@app.get("/api/health", tags=["System"])
def health_check():

    return {
        "status": "ok",
        "message": "Credit Risk AI API is running",
        "models": [
            "XGBoost",
            "CatBoost"
        ]
    }


# ==========================================
# 4. PREDICT
# ==========================================

@app.post(
    "/api/predict/{model_name}",
    tags=["Core AI Operations"]
)
def predict_credit_risk(
    model_name: str,
    customer: CustomerFlow
):

    model_name = model_name.lower()

    # Chuyển dữ liệu Pydantic thành dictionary
    raw_data_dict = customer.model_dump()


    # ======================================
    # XGBOOST
    # ======================================

    if model_name == "xgboost":

        prediction, probability = preprocess_and_predict(
            raw_data_dict=raw_data_dict,
            model=model_safe,
            preprocessor=preprocessor_safe,
            model_type="xgboost",
            threshold=THRESHOLD_SAFE
        )

        strategy = "SAFE"
        threshold = THRESHOLD_SAFE
        display_model = "XGBoost"


    # ======================================
    # CATBOOST
    # ======================================

    elif model_name == "catboost":

        prediction, probability = preprocess_and_predict(
            raw_data_dict=raw_data_dict,
            model=model_sweep,
            preprocessor=preprocessor_sweep,
            model_type="catboost",
            threshold=THRESHOLD_SWEEP
        )

        strategy = "SWEEP"
        threshold = THRESHOLD_SWEEP
        display_model = "CatBoost"


    # ======================================
    # MODEL KHÔNG HỢP LỆ
    # ======================================

    else:

        raise HTTPException(
            status_code=400,
            detail="Model không hợp lệ. Chỉ chấp nhận 'xgboost' hoặc 'catboost'."
        )


    # ======================================
    # RESPONSE
    # ======================================

    risk_probability = round(probability * 100, 2)

    return {
        "status_code": 200,

        "model": display_model,

        "strategy": strategy,

        "risk_probability": risk_probability,

        "threshold": round(threshold * 100, 2),

        "is_bad_loan": bool(prediction),

        "risk_level": (
            "HIGH"
            if prediction == 1
            else "LOW"
        ),

        "recommendation": (
            "Manual Review Recommended"
            if prediction == 1
            else "Eligible for Further Approval Consideration"
        )
    }