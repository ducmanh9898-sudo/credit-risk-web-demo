from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import xgboost as xgb
from catboost import CatBoostClassifier
from inference import preprocess_and_predict 

app = FastAPI(title="Hệ thống Chấm điểm Tín dụng AI")

# ==========================================
# 1. TẢI SẴN TẤT CẢ MÔ HÌNH VÀO RAM LÚC KHỞI ĐỘNG
# ==========================================
print("⏳ Đang tải các mô hình AI vào bộ nhớ...")

# Lõi SAFE (XGBoost)
preprocessor_safe = joblib.load("classic/models/preprocessor_standard.pkl")
model_safe = joblib.load("classic/models/XGBoost_model.pkl")
THRESHOLD_SAFE = 0.5541

# Lõi SWEEP (CatBoost)
preprocessor_sweep = joblib.load("classic/models/preprocessor_native.pkl")
model_sweep = CatBoostClassifier()
model_sweep.load_model("classic/models/CatBoost_model.cbm")
THRESHOLD_SWEEP = 0.3453

print("✅ Tải mô hình hoàn tất!")

# Biến Toàn cục (Global Variable) lưu trữ chiến lược hiện tại đang vận hành
CURRENT_STRATEGY = "SAFE" 


# ==========================================
# 2. CẤU TRÚC DỮ LIỆU FRONTEND
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

class StrategyUpdate(BaseModel):
    strategy: str  # Gửi lên "SAFE" hoặc "SWEEP"


# ==========================================
# 3. CÁC API ENDPOINTS
# ==========================================

@app.post("/api/admin/set_strategy", tags=["Admin Operations"])
def admin_set_strategy(payload: StrategyUpdate):
    """
    API DÀNH CHO ADMIN: Thay đổi chiến lược kinh doanh theo thời gian thực (Không cần Restart).
    """
    global CURRENT_STRATEGY
    new_strategy = payload.strategy.upper()
    
    if new_strategy not in ["SAFE", "SWEEP"]:
        raise HTTPException(status_code=400, detail="Chiến lược không hợp lệ. Chỉ chấp nhận 'SAFE' hoặc 'SWEEP'.")
    
    CURRENT_STRATEGY = new_strategy
    return {
        "status_code": 200,
        "message": f"Thành công! Hệ thống hiện đang chạy với chiến lược: {CURRENT_STRATEGY}"
    }

@app.get("/api/admin/get_strategy", tags=["Admin Operations"])
def admin_get_strategy():
    """
    API DÀNH CHO ADMIN: Xem chiến lược nào đang được kích hoạt.
    """
    return {"current_strategy": CURRENT_STRATEGY}


@app.post("/api/predict_risk", tags=["Core AI Operations"])
def predict_credit_risk(customer: CustomerFlow):
    """
    API DÀNH CHO NGƯỜI DÙNG: Tính toán rủi ro tự động dựa vào chiến lược Admin đã chọn.
    """
    raw_data_dict = customer.dict()
    
    # Bẻ nhánh luồng xử lý tùy theo biến CURRENT_STRATEGY
    if CURRENT_STRATEGY == "SAFE":
        prediction, probability = preprocess_and_predict(
            raw_data_dict=raw_data_dict,
            model=model_safe,
            preprocessor=preprocessor_safe,
            model_type="xgboost",
            threshold=THRESHOLD_SAFE
        )
    else:  # Chiến lược SWEEP
        prediction, probability = preprocess_and_predict(
            raw_data_dict=raw_data_dict,
            model=model_sweep,
            preprocessor=preprocessor_sweep,
            model_type="catboost",
            threshold=THRESHOLD_SWEEP
        )
    
    # Trả kết quả về
    return {
        "status_code": 200,
        "business_strategy_applied": CURRENT_STRATEGY,
        "threat_probability": round(probability * 100, 2),
        "is_bad_loan": bool(prediction),
        "recommendation": "Cảnh báo Rủi ro / Chuyển duyệt thủ công" if prediction == 1 else "Hồ sơ An toàn / Đủ điều kiện duyệt"
    }