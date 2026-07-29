import pandas as pd
import numpy as np

# TỪ ĐIỂN TRUNG BÌNH (TRÍCH XUẤT TỪ TẬP TRAIN)
HOME_INCOME_MEAN = {
    "MORTGAGE": 81168.46,
    "OTHER": 70384.76,
    "OWN": 57950.61,
    "RENT": 55048.44
}

GRADE_LOAN_MEAN = {
    "A": 8583.28,
    "B": 9998.73,
    "C": 9162.15,
    "D": 10644.97,
    "E": 13131.49,
    "F": 14283.85,
    "G": 16208.52
}

def preprocess_and_predict(raw_data_dict, model, preprocessor, model_type, threshold):
    # Lấy các biến gốc
    age = float(raw_data_dict['person_age'])
    income = float(raw_data_dict['person_income'])
    emp_length = float(raw_data_dict['person_emp_length'])
    loan_amnt = float(raw_data_dict['loan_amnt'])
    loan_int_rate = float(raw_data_dict['loan_int_rate'])
    loan_percent_income = float(raw_data_dict['loan_percent_income'])
    
    home_ownership = str(raw_data_dict['person_home_ownership']).upper()
    loan_grade = str(raw_data_dict['loan_grade']).upper()

    # Tính toán các tỷ lệ tài chính & so sánh trung bình
    raw_data_dict['income_per_age'] = income / age if age > 0 else 0
    raw_data_dict['emp_stability_ratio'] = emp_length / (age - 18 + 1e-5)
    raw_data_dict['loan_to_emp_length'] = loan_amnt / (emp_length + 1)
    raw_data_dict['estimated_interest_burden'] = loan_amnt * (loan_int_rate / 100)
    raw_data_dict['is_anomaly_emp'] = 1 if emp_length > (age - 14) else 0
    raw_data_dict['is_extreme_loan'] = 1 if loan_percent_income > 0.5 else 0
    raw_data_dict['income_vs_home_mean'] = income / HOME_INCOME_MEAN.get(home_ownership, 1.0)
    raw_data_dict['loan_vs_grade_mean'] = loan_amnt / GRADE_LOAN_MEAN.get(loan_grade, 1.0)

    # Chuyển đổi thành DataFrame
    df_input = pd.DataFrame([raw_data_dict])
    
    # Đảm bảo đúng 19 cột theo thứ tự
    numeric_cols = [
        'person_age', 'person_income', 'person_emp_length', 'loan_amnt', 'loan_int_rate', 
        'loan_percent_income', 'cb_person_cred_hist_length', 'income_per_age', 
        'emp_stability_ratio', 'loan_to_emp_length', 'estimated_interest_burden', 
        'is_anomaly_emp', 'is_extreme_loan', 'income_vs_home_mean', 'loan_vs_grade_mean'
    ]
    categorical_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
    df_input = df_input[numeric_cols + categorical_cols]

    # Chạy qua Bộ tiền xử lý (Scaler / Encoder)
    X_processed = preprocessor.transform(df_input)
    
    # Ép kiểu đặc thù cho mô hình
    if model_type.lower() == 'catboost':
        cat_idx = list(range(15, 19))
        X_final = np.array(X_processed, dtype=object)
        X_final[:, cat_idx] = X_final[:, cat_idx].astype(int).astype(str)
    else:
        X_final = X_processed

    # Dự đoán và Đánh giá Ngưỡng
    y_probs = model.predict_proba(X_final)[0, 1]
    y_predict = 1 if y_probs >= threshold else 0

    return y_predict, y_probs