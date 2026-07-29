# 🚀 Hướng dẫn Cài đặt & Vận hành Pipeline API

Tài liệu này cung cấp cái nhìn tổng quan về luồng dữ liệu (Data Flow) và các bước để khởi chạy Server API của Hệ thống Chấm điểm Tín dụng.

## 🔄 1. Sơ đồ Luồng Dữ liệu (Data Flow Blueprint)

Quá trình từ khi Frontend gửi dữ liệu cho đến khi nhận kết quả được thực hiện hoàn toàn khép kín thông qua Backend API.

```text
[ FRONTEND / UI ] 
       │
       ▼ (Gửi JSON 11 trường gốc)
[ BACKEND API: main.py ]
       │
       ▼ (Gọi hàm preprocess_and_predict)
[ INFERENCE SCRIPT: inference.py ]
       ├─► 1. Tính toán Tỷ lệ tài chính (8 biến mới)
       ├─► 2. Đối chiếu Từ điển (Income/Home & Loan/Grade)
       ├─► 3. Ghép mảng 19 chiều (15 Số + 4 Phân loại)
       │
       ▼ (Gọi File Dịch thuật từ classic/models/)
[ PREPROCESSOR: StandardScaler & Encoders ]
       │
       ▼ (Ma trận số thực)
[ AI MODEL: XGBoost / CatBoost ]
       │
       ▼ (Sinh xác suất Rủi ro)
[ THRESHOLD FILTER: > 0.5541 hoặc > 0.3453 ]
       │
       ▼ (Kết luận: 1 hoặc 0)
[ BACKEND API ] ──► [ FRONTEND / UI ] (Hiển thị Kết quả)
```

## 🛠️ 2. Quy trình Cài đặt (Setup Pipeline)

**Bước 1: Chuẩn bị Thư mục & Môi trường**
```text
Kiểm tra cấu trúc dự án. Bạn phải chắc chắn thư mục classic/models/ có chứa tệp mô hình (.pkl, .cbm).

Sau đó cài file requirements.txt
```

**Bước 2: Thiết lập Chiến lược Kinh doanh (Business Strategy)**
```text
1. Khi Server chạy, mặc định nó sẽ ở trạng thái SAFE.

2. Người lập trình Frontend có thể thiết kế một "Nút gạt (Toggle)" trên trang Quản trị viên (Admin Dashboard).

3. Khi Admin gạt nút sang "Quét Sạch Rủi Ro", Frontend chỉ cần bắn một Request chứa JSON {"strategy": "SWEEP"} vào endpoint /api/admin/set_strategy.

4. Ngay lập tức, luồng người dùng ở Endpoint /api/predict_risk sẽ tự động được xoay chiều qua mô hình CatBoost mà người dùng không hề hay biết!
```
**Bước 3: Khởi động Máy chủ (Start Server)**
```text
Khởi động FastAPI server thông qua Uvicorn:
       uvicorn main:app --reload

Ghi chú: Cờ --reload giúp Server tự động cập nhật nếu bạn có chỉnh sửa file code.
```

**Bước 4: Kiểm thử API (Testing)**
```text
Mở trình duyệt, truy cập: http://localhost:8000/docs

Mở Endpoint POST /api/predict_risk, bấm "Try it out".

Paste đoạn JSON dữ liệu khách hàng vào ô Request Body.

Bấm "Execute" và xem trực tiếp kết quả trả về (threat_probability và is_bad_loan).
```