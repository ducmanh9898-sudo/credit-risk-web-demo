# 🔬 Phân hệ Nghiên cứu Lượng tử (Quantum Research Module)

Chào mừng bạn đến với Không gian Lai Lượng tử - Cổ điển (Hybrid Quantum-Classical Space). Đây không phải là một hệ thống độc lập thay thế cho Web API Cổ điển ở thư mục bên ngoài, mà là một **Công trình Nghiên cứu Nâng cao (Innovation Point)** được đính kèm nhằm chứng minh tiềm năng đột phá của Trí tuệ Nhân tạo Lượng tử (Quantum AI) trong bài toán Đánh giá Rủi ro Tín dụng.

---

## 🧬 1. Khác biệt Cốt lõi về Kiến trúc: QCNN là Trái tim
Điểm sáng tạo nhất của phương pháp lai này nằm ở luồng Dữ liệu Đầu vào (Input Features). Thay vì sử dụng con người để thiết kế các đặc trưng phức tạp, chúng tôi nhường việc đó cho Mạch Lượng tử!

*   **Kiến trúc Cổ điển (Classic Framework):** Mô hình được nuôi bằng **19 biến**, trong đó bao gồm 11 biến gốc (Original) và 8 biến xào nấu thủ công (Hand-crafted Feature Engineering do con người thiết kế).
*   **Kiến trúc Lượng tử (Quantum Framework):** Mô hình giữ nguyên 11 biến gốc, nhưng 8 biến còn lại không do con người xào nấu. Dữ liệu thô được đưa qua một **Mạng Nơ-ron Tích chập Lượng tử (QCNN)**. Lúc này, QCNN đóng vai trò như một **Quantum Feature Extractor (Bộ trích xuất Đặc trưng Lượng tử)**. Nó ánh xạ các biến số vào không gian Hilbert phức hợp, tìm ra các mối tương quan phi tuyến tính siêu việt, và "ép" ra 8 Đặc trưng Lượng tử ưu việt nhất để đưa cho mô hình Cổ điển (XGBoost, CatBoost,...) phân loại.

> [!TIP]
> Việc dùng QCNN làm *Feature Extractor* chứng minh rằng Lượng tử có thể tự động hóa và vượt qua trí tuệ con người trong việc biểu diễn Dữ liệu Khách hàng mà không cần phải thay đổi toàn bộ hạ tầng dự đoán! (Bạn có thể xem trọng số của bộ trích xuất này tại thư mục `qcnn_feature_extractor/`).

---

## 📊 2. Phân tích Ưu thế của Lượng tử (Kết quả Khảo nghiệm)

Chúng tôi đã tiến hành huấn luyện 7 mô hình SOTA (State-Of-The-Art) mạnh nhất hiện nay trên cả 2 kiến trúc (Classic và Quantum) để đối chiếu công bằng. Dưới đây là Bảng điều khiển (Dashboard) so sánh tổng hợp:

![Quantum vs Classic Dashboard](./quantum-classic%20-%20analysis/Quantum_vs_Classic_Dashboard_analysis.png)

Từ Dashboard trên, chúng ta rút ra những Khám phá Khoa học (Key Findings) đắt giá:

### 🛡️ Khi ép Precision Cao (Chiến thuật "An Toàn Tối Đa")
Khi ngân hàng yêu cầu hệ thống phải cực kỳ thận trọng (ép Precision ≥ 0.90 để không từ chối nhầm người tốt), Lượng tử thể hiện sự **ổn định tuyệt đối**. 
*   **Biểu đồ 3:** Recall của Quantum duy trì ở mức ngang ngửa, thậm chí nhỉnh hơn Classic ở một số thuật toán lõi. Điều này chứng tỏ Quantum không hề bị hụt hơi hay phải hy sinh Recall quá nhiều để đạt được Precision cao như các mô hình thông thường.

### 🧹 Khi ép Recall Cao (Chiến thuật "Quét Sạch Rủi Ro")
Đây chính là nơi **sức mạnh của Lượng tử tỏa sáng rực rỡ nhất**!
Khi ngân hàng yêu cầu hệ thống phải "vét cạn" nợ xấu (ép Recall ≥ 0.90 hoặc 0.85), các mô hình Cổ điển thường phải trả giá bằng việc báo động nhầm (False Positives) rất nhiều.
*   **Biểu đồ 4 & 5:** Lượng tử (Đường màu Xanh) cho ra chỉ số **Precision cao hơn hẳn** Cổ điển (Đường màu Vàng) trên hầu hết các mặt trận. 
*   **Ý nghĩa Thực tiễn:** Việc có Precision cao hơn ở mức Recall khắt khe đồng nghĩa với việc ngân hàng sẽ giảm thiểu được hàng chục ngàn hồ sơ bị báo động nhầm. Hệ thống Lượng tử giúp tiết kiệm chi phí và hàng ngàn giờ thẩm định thủ công cho đội ngũ tín dụng, trong khi vẫn không để lọt nợ xấu!

---

## 📂 3. Cấu trúc Tài liệu trong Phân hệ
Bạn có thể tự tay chạy lại các khảo nghiệm này thông qua các tài nguyên được cung cấp:

*   **`notebooks/`**: Chứa toàn bộ mã nguồn huấn luyện. Đáng chú ý là `attacker-2026 - hyper_hybrid.ipynb` (Siêu Notebook huấn luyện cả 7 mô hình Lượng tử) và `attacker-2026 - analysis_charts.ipynb` (Notebook sinh ra Dashboard trên).
*   **`qcnn_feature_extractor/`**: Nơi lưu trữ trọng số mạch lượng tử đã được nén (`best_model.pth`).
*   **`quantum-classic - analysis/`**: Các file Excel thô chứa số liệu chi tiết tới từng chữ số thập phân của quá trình benchmark.