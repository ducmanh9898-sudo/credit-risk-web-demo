# 🏦 Hệ thống Đánh giá Rủi ro Tín dụng (Credit Risk Scoring API)
**Lõi Trí tuệ Nhân tạo (AI Core) & Tài liệu Tích hợp cho Web Developer**

---

## 🌟 1. Mục đích của Kho lưu trữ (Repository Purpose)
Kho lưu trữ (GitHub Repository) này được xây dựng nhằm hai mục đích cốt lõi:
1. **Minh bạch Nghiên cứu AI:** Trình bày chi tiết luồng tiền xử lý dữ liệu (Feature Engineering), quá trình huấn luyện và đánh giá các mô hình Học máy Cổ điển (SOTA) kết hợp tư duy Lai Lượng tử - Cổ điển.
2. **Cầu nối Triển khai (Web Integration):** Trợ giúp các lập trình viên Backend / Web Developer hiểu rõ cách mô hình hoạt động. Cung cấp sẵn các đoạn mã nguồn chuẩn mực để tích hợp AI vào nền tảng Web/App một cách nhanh chóng nhất (Plug-and-Play) mà không cần phải hiểu sâu về thuật toán.

---

## 🎯 2. Tổng quan Dự án (Project Overview)
Dự án này cung cấp hệ thống AI phân loại rủi ro tín dụng / nợ xấu (Credit Risk) thông qua Dữ liệu Bảng (Tabular Data). Hệ thống được thiết kế để đánh giá từng khách hàng độc lập (Sample Testing) dựa trên 11 trường thông tin đầu vào.

Thay vì sử dụng một ranh giới quyết định (Threshold) mặc định là `0.5`, hệ thống cung cấp **2 lõi mô hình độc lập** đại diện cho 2 chiến thuật kinh doanh kiểm soát rủi ro khác nhau. Hệ thống Web có thể cấu hình để gọi 1 trong 2 mô hình sau:

*   🛡️ **Chiến lược "An Toàn Tối Đa" (Áp đảo Precision) - Sử dụng XGBoost**
    *   **Ngưỡng kích hoạt:** `0.5541`
    *   **Bộ Tiền xử lý yêu cầu:** `preprocessor_standard.pkl`
    *   **Mục đích:** Khi hệ thống trả về cảnh báo "Nợ xấu", độ chính xác là cực kỳ cao. Phù hợp cho kịch bản ngân hàng muốn từ chối tự động các hồ sơ rủi ro cao mà không sợ từ chối nhầm người vay tốt.

*   🧹 **Chiến lược "Quét Sạch Rủi Ro" (Áp đảo Recall) - Sử dụng CatBoost**
    *   **Ngưỡng kích hoạt:** `0.3453`
    *   **Bộ Tiền xử lý yêu cầu:** `preprocessor_native.pkl`
    *   **Mục đích:** Chấp nhận nguyên tắc "thà bắt nhầm còn bỏ sót". Phù hợp để tạo bộ lọc khắt khe, khoanh vùng mọi hồ sơ có rủi ro tiềm ẩn để chuyển cho nhân viên tín dụng đánh giá thủ công.

---

## 📥 3. Payload Đầu vào từ UI (Raw Inputs)

Frontend (Giao diện web/form nhập liệu) **chỉ cần thu thập 11 trường thông tin gốc** của khách hàng. Backend sẽ nhận Payload JSON với cấu trúc chuẩn như sau:

```json
{
  "person_age": 25,
  "person_income": 50000,
  "person_emp_length": 3,
  "loan_amnt": 15000,
  "loan_int_rate": 10.5,
  "loan_percent_income": 0.3,
  "cb_person_cred_hist_length": 4,
  "person_home_ownership": "RENT",
  "loan_intent": "EDUCATION",
  "loan_grade": "B",
  "cb_person_default_on_file": "N"
}
```

---

## 🚀 4. Cấu trúc Thư mục Triển khai (Deployment Setup)

Để tích hợp thành công, Backend Developer chỉ cần tập trung vào thư mục models/ và các tệp mã nguồn Python đi kèm được cung cấp trong kho lưu trữ này:

```json
{
📦 project-root
 ┣ 📂 classic/                      # KHÔNG GIAN HỌC MÁY CỔ ĐIỂN (Đang vận hành)
 ┃ ┣ 📂 data/                       # Dữ liệu & Data dictionary
 ┃ ┣ 📂 notebooks/                  # Notebooks huấn luyện (XGBoost, CatBoost...)
 ┃ ┗ 📂 models/                 
 ┃   ┣ 📜 XGBoost_model.pkl         # Trọng số XGBoost (Chiến lược SAFE)
 ┃   ┣ 📜 CatBoost_model.cbm        # Trọng số CatBoost (Chiến lược SWEEP)
 ┃   ┣ 📜 preprocessor_standard.pkl # Bộ dịch thuật dữ liệu (BẮT BUỘC cho XGBoost)
 ┃   ┗ 📜 preprocessor_native.pkl   # Bộ dịch thuật dữ liệu (BẮT BUỘC cho CatBoost)
 ┃
 ┣ 📂 quantum/                      # KHÔNG GIAN LAI LƯỢNG TỬ (Định hướng tương lai)
 ┃ ┣ 📂 data/                       # (Hiện tại để trống)
 ┃ ┣ 📂 notebooks/                  # (Hiện tại để trống)
 ┃ ┗ 📂 models/                     # (Hiện tại để trống)
 ┃
 ┣ 📜 inference.py                  # Script chứa hàm tính toán & tiền xử lý tự động
 ┣ 📜 main.py                       # File chạy Server API (VD: FastAPI)
 ┗ 📜 requirements.txt              # Danh sách thư viện môi trường
}
```

---

## 🧮 5. Hướng dẫn Tích hợp & Đặc tả Code (Integration Guide)

Nhóm phát triển phần mềm sử dụng các tệp tin được cung cấp để thiết lập API theo luồng logic sau:

### 5.1. Thiết lập môi trường (requirements.txt)

```text
Tệp này chỉ trích xuất chính xác các thư viện cốt lõi cần thiết để chạy Model (như xgboost, catboost, scikit-learn, fastapi, pandas...) nhằm giúp Server Backend hoạt động nhẹ bén, không bị phình to (bloated).
👉 Cài đặt bằng lệnh: pip install -r requirements.txt
```

### 5.2. Logic Tiền xử lý tự động (inference.py)

```text
Đây là "trái tim" xử lý dữ liệu của hệ thống trước khi đưa vào AI. Hàm preprocess_and_predict() bên trong tệp này sẽ tự động thực hiện các tác vụ:

1. Feature Engineering: Nhận 11 trường gốc từ JSON và tự động nội suy ra 8 biến nâng cao (Tổng cộng 19 biến). Các phép tính bao gồm tỷ lệ tài chính, cờ cảnh báo (1/0), và đối chiếu hệ số trung bình dựa trên bộ Từ điển tĩnh (Dictionary) có sẵn trong code.

2. Dịch thuật Dữ liệu (Scaling/Encoding): Chạy mảng 19 biến qua tệp preprocessor_*.pkl tương ứng để biến các trường phân loại (Text) thành Ma trận Số (Numeric) mà AI có thể hiểu được. Ép kiểu dữ liệu đặc thù nếu sử dụng CatBoost.

3. Dự đoán: Trả về xác suất rủi ro (y_probs) và áp dụng ngưỡng rủi ro (Threshold) để chốt kết quả Cảnh báo cuối cùng (y_predict).
```

### 5.3. Khởi tạo API Server (main.py)

```text
Tệp này cung cấp cấu trúc mẫu bằng framework FastAPI để gọi hàm từ inference.py. Logic vận hành bao gồm:

1. Load các tệp Model và Preprocessor một lần duy nhất lúc khởi động Server (tối ưu hóa tốc độ xử lý).

2. Tạo Endpoint (ví dụ: /api/predict_risk) để đón nhận JSON payload từ Frontend.

3. Chạy dữ liệu qua pipeline và trả về JSON Response cuối cùng cho Frontend hiển thị (bao gồm: Mã trạng thái, Chiến lược đang dùng, % Rủi ro, và Khuyến nghị hệ thống).

👉 Khởi động Server thử nghiệm bằng lệnh: uvicorn main:app --reload```