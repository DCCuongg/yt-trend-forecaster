# 📈 Báo Cáo Đánh Giá Mô Hình Dự Báo Xu Hướng (YouTube Trend Forecaster)

Tài liệu này tổng hợp cấu trúc dữ liệu tầng **Gold (Time-Series Aggregation)** và kết quả nghiệm thu mô hình **LightGBM Regressor** trên tập kiểm thử 14 ngày (**Test Horizon = 14 ngày**).

---

## 1. Cấu Trúc Dữ Liệu Tầng Gold (Feature Store / Time-Series)

Dữ liệu được chuẩn hóa và tổng hợp từ tầng Silver (chống trùng lặp lượt xem đa quốc gia trong cùng ngày).

### Mẫu dữ liệu thực tế (Chủ đề: *Autos & Vehicles*)

| Ngày (`ds`) | Tên chủ đề (`topic_name`) | Loại (`topic_type`) | Lượt xem (`total_views`) | Lượt thích (`total_likes`) | Lượt bình luận (`total_comments`) | Số video Trending | Độ phủ quốc gia (`total_country_appearances`) | Tỷ lệ tương tác (`engagement_rate`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2024-10-12 | Autos & Vehicles | CATEGORY | 62,670,000 | 2,634,696 | 158,124 | 81 | 183 | 4.46% |
| 2024-10-13 | Autos & Vehicles | CATEGORY | 61,494,957 | 2,564,864 | 158,784 | 84 | 179 | 4.43% |
| 2024-10-14 | Autos & Vehicles | CATEGORY | 65,036,777 | 2,677,800 | 158,520 | 83 | 177 | 4.36% |
| 2024-10-15 | Autos & Vehicles | CATEGORY | 68,684,609 | 2,839,793 | 170,984 | 91 | 184 | 4.38% |
| 2024-10-16 | Autos & Vehicles | CATEGORY | 71,842,351 | 3,046,086 | 185,907 | 90 | 180 | 4.50% |
| 2024-10-17 | Autos & Vehicles | CATEGORY | 74,318,549 | 3,180,366 | 199,798 | 90 | 198 | 4.55% |
| 2024-10-18 | Autos & Vehicles | CATEGORY | 78,669,697 | 3,439,004 | 199,532 | 90 | 205 | 4.63% |
| 2024-10-19 | Autos & Vehicles | CATEGORY | 79,805,640 | 3,476,795 | 194,977 | 81 | 178 | 4.60% |
| 2024-10-20 | Autos & Vehicles | CATEGORY | 72,858,029 | 3,239,667 | 182,320 | 77 | 179 | 4.70% |
| 2024-10-21 | Autos & Vehicles | CATEGORY | 76,679,720 | 3,734,737 | 212,377 | 77 | 168 | 5.15% |

* **Độ phủ quốc gia (`total_country_appearances`):** Đo lường mức độ lan tỏa toàn cầu bằng tổng số lượt lọt top thịnh hành của các video thuộc chủ đề trên mọi quốc gia.
* **Tỷ lệ tương tác (`engagement_rate`):** Tỷ lệ người xem thực hiện tương tác chủ động (Like + Comment) trên tổng lượt xem.

---

## 2. Kết Quả Đánh Giá Mô Hình (14-Day Test Horizon)

Mô hình được huấn luyện với hàm mục tiêu kháng ngoại lai (`objective="regression_l1"`) trên biến đổi `log1p(total_views)`.

| Chỉ số đánh giá | Giá trị | Đơn vị | Ý nghĩa thực nghiệm |
| :--- | :---: | :---: | :--- |
| **MAE** *(Sai số tuyệt đối TB)* | **4,745,122** | Lượt xem (Views) | Độ lệch trung bình mỗi ngày giữa dự báo và thực tế trên toàn bộ các chủ đề. |
| **RMSE** *(Sai số bình phương căn)* | **16,884,786** | Lượt xem (Views) | Chịu ảnh hưởng bởi các cú bùng nổ lượt xem đột biến (viral shock) của các Category lớn (*Music*, *Entertainment*). |
| **MAPE** *(Tỷ lệ sai số phần trăm)* | **17.09%** | % | Thuộc nhóm mô hình dự báo **Tốt (< 20%)** đối với dữ liệu chuỗi thời gian phân tán cao. |
| **Peak Timing Error** *(Lệch ngày đỉnh)* | **± 2.22** | Ngày | Khả năng dự báo điểm rơi đạt đỉnh xu hướng trong khung 2 tuần với độ trễ chỉ quanh mức 2 ngày. |

---

## 3. Nhận Xét & Định Hướng Triển Khai

* **Bắt nhịp xu hướng tốt:** Đường dự báo bám sát chu kỳ tăng giảm của các chủ đề lớn; sai số lệch đỉnh $\pm 2.22$ ngày mang lại giá trị cao cho việc lập kế hoạch đón đầu xu hướng nội dung.
* **Tính chất dữ liệu theo tần suất:** Do đặc thù lượt xem hằng ngày (Daily) chịu tác động của thuật toán đề xuất ngắn hạn, sai số ngày đơn lẻ tồn tại tính nhiễu. Khi tổng hợp theo tuần (Weekly) hoặc tháng (Monthly), các sai số ngẫu nhiên tự bù trừ và độ chính xác dự báo sẽ tăng lên đáng kể.
* **Trọng số & Metadata:** Toàn bộ artifact mô hình (`lgbm_trend_forecaster_14day.pkl`, `model_metadata.json`) đã được đồng bộ trực tiếp lên Hugging Face Model Hub sẵn sàng cho Backend API phục vụ dashboard.

https://huggingface.co/datasets/cuongduongok/yt-trend-forecaster-gold-data/tree/main

https://huggingface.co/cuongduongok/yt-trend-forecaster-models/tree/main