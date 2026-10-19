# yt-trend-forecaster
**Đồ án môn Công Nghệ Dữ Liệu Lớn**

# Tóm tắt Ý Tưởng và Nền tảng Triển khai

## 1. Nền tảng Triển khai & Kiến trúc Hạ tầng

**Quản lý Model trên Hugging Face Hub**
Lưu trữ toàn bộ trọng số mô hình (`.pkl`, `.pt`, `.json`) trên Hugging Face Model Hub thay vì GitHub để tránh giới hạn dung lượng 100MB và băng thông Git LFS. 

**Kiến trúc Data Lake (Medallion Architecture chi phí 0đ)**
Kiến trúc Data Lake (Medallion 0đ): Xử lý trực tiếp trên Google Colab thay vì đẩy dữ liệu thô lên Azure nhằm tránh phí băng thông (Egress cost) và độ trễ đa đám mây. Quy trình gồm 3 tầng: tải file Parquet từ Kaggle qua kagglehub (Bronze), dùng PySpark gom nhóm thành chuỗi thời gian theo ngày/tuần (Silver & Gold), và lưu bản sạch lên Hugging Face hoặc.

**Cơ sở dữ liệu Django + PostgreSQL Cloud (Neon.tech / Supabase)**
Sử dụng PostgreSQL Cloud miễn phí.

**Cơ chế Thực thi Backend "Hybrid" (Local & Remote Colab)**
Thiết kế tầng suy luận (Inference Service) độc lập cho phép chuyển đổi linh hoạt thông qua biến môi trường `INFERENCE_MODE`. Ở chế độ mặc định (`LOCAL`), Django tự tải mô hình nhẹ từ Hugging Face về RAM để dự báo trực tiếp; khi cần chạy mô hình học sâu hoặc quét NLP nặng (`REMOTE`), hệ thống tự động chuyển tiếp yêu cầu qua API (FastAPI + Ngrok/Cloudflare Tunnel) để mượn tài nguyên GPU trên Google Colab và nhận kết quả JSON trả về.

---

## 2. Tóm tắt Ý tưởng Nghiên cứu

**Phạm vi bài toán (Problem Scope)**
Xây dựng hệ thống phân tích dữ liệu lớn dự báo chuỗi thời gian (Time-Series Forecasting) cho vòng đời các chủ đề thịnh hành trên YouTube dựa trên bộ dữ liệu *YouTube Trending Video Dataset* (định dạng Parquet từ Kaggle). Hệ thống khai thác lịch sử tương tác (lượt xem, thích, bình luận), siêu dữ liệu văn bản (tiêu đề, tags, danh mục) và mốc thời gian nhằm mô hình hóa quy luật vận động, dự đoán thời điểm bùng nổ tiếp theo và quy mô lưu lượng truy cập dự kiến.

**Phương pháp đề xuất và Phân tích trọng tâm**
* **Đặt vấn đề:** Tự động phát hiện quy luật chu kỳ ẩn giấu của các chủ đề chỉ thông qua lịch sử biến động lưu lượng nội tại bằng cách chuyển đổi dữ liệu video rời rạc thành hàng loạt đồ thị chuỗi thời gian theo danh mục và từ khóa.
* **Tiền xử lý dữ liệu:** Tận dụng trường danh mục (`video_category_id`) sạch để gom nhóm vĩ mô, đồng thời tách chuỗi thẻ từ khóa (`video_tags`) theo dấu phẩy và trích xuất bổ sung từ khóa từ tiêu đề đối với các bản ghi bị khuyết thẻ nhằm tránh đứt gãy chuỗi lịch sử.
* **Kỹ thuật huấn luyện trọng tâm:** Kết hợp 3 phương pháp: (1) Phân rã chuỗi thời gian và Hồi quy cộng tính để tách xu hướng dài hạn, chu kỳ tự nhiên và điểm đột biến; (2) Biến đổi miền tần số và Phân tích tự tương quan để đo khoảng cách lặp lại giữa các đỉnh lượt xem dài hạn; (3) Hồi quy học máy trên cửa sổ trượt (Random Forest, Gradient Boosting) và Mạng nơ-ron học sâu chuỗi thời gian để học hình dáng đường cong lượt xem ngay trước thời điểm bùng nổ.
* **Nhánh phân tích bổ trợ:** Theo dõi độ dốc đồ thị để phát hiện điểm đột biến (nhận diện chủ đề đang tăng trưởng nóng), kết hợp hồi quy phi tuyến và độ tương đồng nội dung để chấm điểm tiêu đề và gợi ý từ khóa theo danh mục.

**Dự kiến kết quả đạt được (Expected Results)**
Hoàn thiện đường ống dữ liệu (Data Pipeline) xử lý dữ liệu lớn và mô hình dự báo chuỗi thời gian chính xác, được kiểm chứng qua các chỉ số MAE, RMSE và MAPE trên tập kiểm thử chia theo thời gian (Time-based Split). Đồng thời, xây dựng thành công giao diện Dashboard trực quan hóa biểu đồ dự báo tương lai, kèm theo các công cụ thống kê từ khóa tăng trưởng nóng, chấm điểm tiêu đề và gợi ý ngách chủ đề tiềm năng.

**Kết luận dự kiến và Hướng phát triển (Conclusion & Future Work)**
Khẳng định tính khả thi của việc kết hợp khai phá văn bản và chuỗi thời gian để dự báo định lượng xu hướng YouTube, thay thế phương pháp phán đoán cảm tính truyền thống. Kiến trúc hệ thống tạo nền tảng mở rộng linh hoạt sang các bài toán chuyên sâu như gom cụm chủ đề ẩn bằng NLP, phát hiện đột biến lưu lượng thời gian thực (Trend Spike Detection), phân loại cấp độ lan tỏa của tiêu đề (Virality Tier Classification) và gợi ý nội dung cá nhân hóa cho từng kênh.
# Kiến trúc thư mục dự án.

Kiến trúc này tách biệt rõ ràng 3 khối: Big Data & AI Pipeline, Backend (Django), và Frontend (React/Next.js), đồng thời tách riêng Level 1 (Core) và Level 2 (Extension - Plug & Play) để nếu không kịp làm Level 2 thì hệ thống vẫn chạy hoàn hảo, không bị lỗi import.

## Kiến trúc tổng quan repo.
```
yt-trend-forecaster/
├── README.md                         # Tài liệu hướng dẫn chạy dự án & sơ đồ kiến trúc
├── .gitignore                        # Bỏ qua venv, node_modules, .env, file parquet/model nặng
├── docker-compose.yml                # Chạy nhanh toàn bộ hệ thống ở máy local
├── docs/                             # Tài liêu kiểm chứng và phát triển.
│
├── data_and_ml/                      # [KHỐI 1] XỬ LÝ BIG DATA & HUẤN LUYỆN MODEL
│   ├── configs/
│   │   └── pipeline_config.yaml      # Cấu hình đường dẫn Kaggle, HF Repo ID, tham số model
│   ├── notebooks/                    # Lưu bản chuẩn các file chạy trên Google Colab
│   │   ├── 01_spark_etl_pipeline.ipynb       # PySpark đọc Parquet, tách tags, gom nhóm chuỗi thời gian
│   │   ├── 02_train_forecasting.ipynb        # Train Prophet / LightGBM / LSTM & đánh giá MAE, RMSE
│   │   ├── 03_topic_and_spike_mining.ipynb   # (Bổ trợ) LDA gom cụm & phát hiện đột biến
│   │   └── 04_colab_remote_worker.ipynb      # Notebook biến Colab thành Server tính toán phụ trợ cho Local
│   ├── src/                          # Source code Python thuần (để import vào notebook hoặc chạy script)
│   │   ├── __init__.py
│   │   ├── spark_processor.py        # Hàm làm sạch video_tags rỗng, nối title + category
│   │   ├── feature_engineering.py    # Biến đổi Fourier, tính Autocorrelation, cắt cửa sổ trượt
│   │   ├── trainers.py               # Code huấn luyện model
│   │   └── hf_hub_manager.py         # Script tự động push/pull model và dataset sạch lên Hugging Face
│   └── requirements-ml.txt           # Thư viện cho Colab (pyspark, prophet, lightgbm, huggingface_hub...)
│
├── backend/                          # [KHỐI 2] DJANGO 
└── frontend/                         # [KHỐI 3] GIAO DIỆN DASHBOARD TRỰC QUAN HÓA
```

## Kiến trúc backend
```
├── backend/                          # [KHỐI 2] DJANGO REST API & BẢO MẬT HỆ THỐNG
│   ├── manage.py
│   ├── .env.example                  # Mẫu biến môi trường (SECRET_KEY, DB_URL, HF_TOKEN, WORKER_API_KEY)
│   ├── requirements-backend.txt      # django, drf, djangorestframework-simplejwt, django-cors-headers...
│   │
│   ├── core/                         # Cấu hình hệ thống & Bảo mật toàn cục
│   │   ├── __init__.py
│   │   ├── settings.py               # Cấu hình DB, CORS, JWT, Throttling (Chống spam request)
│   │   ├── urls.py                   # Định tuyến gốc (/api/v1/auth, /api/v1/reports...)
│   │   ├── wsgi.py & asgi.py         # Cổng giao tiếp máy chủ (Gunicorn/Uvicorn)
│   │   └── permissions.py            # [BẢO MẬT] Custom Permissions dùng chung (IsOwner, IsVerifiedUser, VerifyColabKey)
│   │
│   ├── apps/                         # Chia theo từng Module nghiệp vụ độc lập
│   │   ├── accounts/                 # [NGHIỆP VỤ 1] Quản lý Định danh & Bảo mật Người dùng
│   │   │   ├── migrations/
│   │   │   ├── models.py             # Custom User Model, quản lý Role & hạn mức (Quota) gọi dự báo
│   │   │   ├── serializers.py        # Mã hóa mật khẩu (Hashing), Validate dữ liệu Đăng ký/Đăng nhập
│   │   │   ├── views.py              # API Login/Logout, Cấp phát & Làm mới JWT Token
│   │   │   ├── urls.py               # Route: /login, /register, /token/refresh, /profile
│   │   │   └── admin.py              # Quản trị User trên trang Django Admin
│   │   │
│   │   ├── reports_l1/               # [NGHIỆP VỤ 2 - LEVEL 1] Dự báo Chuỗi thời gian & Báo cáo
│   │   │   ├── migrations/
│   │   │   ├── models.py             # Bảng TrendReport (Gắn khóa ngoại User để cô lập dữ liệu cá nhân)
│   │   │   ├── serializers.py        # Kiểm duyệt tham số đầu vào & đóng gói JSON biểu đồ
│   │   │   ├── views.py              # API CRUD Report (Áp dụng IsAuthenticated & IsOwner permission)
│   │   │   ├── urls.py               # Route: /predict, /history, /export
│   │   │   └── services/             # Tách biệt Logic nghiệp vụ (Business Logic Layer)
│   │   │       ├── inference_router.py  # Điều hướng Local/Colab (Đính kèm Secret Header bảo mật)
│   │   │       └── local_predictor.py   # Load model từ cache & chạy dự báo
│   │   │
│   │   └── channel_advisor_l2/       # [NGHIỆP VỤ 3 - LEVEL 2] Phân tích Kênh & Gợi ý Trend
│   │       ├── migrations/
│   │       ├── models.py             # Lưu lịch sử quét kênh
│   │       ├── serializers.py        # Validate URL/Channel ID (Chống SSRF / Malformed input)
│   │       ├── views.py              # API phân tích kênh (Giới hạn Rate Limit tránh cạn Quota YouTube API)
│   │       ├── urls.py               # Route: /analyze-channel, /niche-recommend
│   │       └── services/
│   │           ├── youtube_scraper.py   # Gọi YouTube Data API v3 an toàn qua API Key ẩn
│   │           └── similarity_engine.py # Tính độ tương đồng Cosine/TF-IDF
│   │
│   └── model_cache/                  # Lưu tạm file trọng số Model tải từ Hugging Face
```

## Kiến Trúc frontend.
```
frontend/
    ├── package.json
    ├── vite.config.js                # Hoặc webpack.config.js
    ├── public/                       # Favicon, static assets
    └── src/
        ├── assets/                   # Hình ảnh, icons, global CSS / Tailwind setup
        ├── components/
        │   ├── common/               # Các component dùng chung (Button, Modal, Table, Card, Loading)
        │   ├── charts/               # Các biểu đồ cốt lõi (Dự báo tương lai, Phân rã mùa vụ, Độ dốc)
        │   └── layout/               # Sidebar, Navbar, AppLayout, khung quản lý tài khoản
        ├── context/                  # React Context (AuthContext, ThemeContext, DashboardFilterContext)
        ├── hooks/                    # Custom hooks (useAuth, useDebounce, useFetchData)
        ├── pages/
        │   ├── Auth/                 # Đăng nhập / Đăng ký
        │   ├── DashboardL1/          # [LEVEL 1] Trang tạo dự báo chủ đề & Kho lưu trữ Report
        │   └── ChannelAdvisorL2/     # [LEVEL 2] Trang khám phá ngách YouTube
        ├── routes/                   # Cấu hình định tuyến (PrivateRoute, AppRoutes)
        ├── services/
        │   └── api.js                # Axios instance cấu hình interceptors (JWT, Base URL)
        ├── utils/                    # Các hàm tiện ích (formatNumber, formatDate, chartDataTransformer)
        ├── constants/                # Hằng số (API paths, color themes cho biểu đồ)
        ├── App.jsx                   # Component gốc chứa Router
        └── main.jsx                  # Điểm khởi chạy React DOM
```
# Các bước triển khai dự án.

# Hướng dẩn cài đặt, chính sách và môi trường

## Khởi tại dựa án

