-- 1. Ràng buộc Check Constraints
ALTER TABLE accounts_customuser
ADD CONSTRAINT chk_user_role CHECK (
    role IN ('STUDENT', 'CREATOR', 'ADMIN')
),
ADD CONSTRAINT chk_user_prediction_quota CHECK (prediction_quota >= 0),
ADD CONSTRAINT chk_user_used_quota CHECK (
    used_quota >= 0
    AND used_quota <= prediction_quota
);

ALTER TABLE reports_l1_trendreport
ADD CONSTRAINT chk_trendreport_status CHECK (
    status IN ('DRAFT', 'READY', 'ARCHIVED')
);

ALTER TABLE reports_l1_marketresearchitem
ADD CONSTRAINT chk_model_type CHECK (
    model_type IN (
        'LGBM_14DAY',
        'PROPHET_QUARTER',
        'LSTM_YEAR'
    )
),
ADD CONSTRAINT chk_execution_status CHECK (
    status IN (
        'PENDING',
        'PROCESSING',
        'SUCCESS',
        'FAILED'
    )
),
ADD CONSTRAINT chk_horizon_days CHECK (horizon_days > 0),
ADD CONSTRAINT chk_execution_duration CHECK (execution_duration_ms >= 0);

-- 2. Đánh chỉ mục Index tối ưu hóa truy vấn
-- Index phục vụ lọc và sắp xếp lịch sử report theo user
CREATE INDEX IF NOT EXISTS idx_trendreport_user_created ON reports_l1_trendreport (user_id, created_at DESC);

-- Index phục vụ tìm kiếm topic và chuỗi thời gian phân tích
CREATE INDEX IF NOT EXISTS idx_marketresearch_topic_date ON reports_l1_marketresearchitem (topic_name, target_date);

-- Index lọc theo trạng thái xử lý model
CREATE INDEX IF NOT EXISTS idx_marketresearch_status ON reports_l1_marketresearchitem (status);

-- GIN Index cho trường JSONB forecast_result (cho phép query theo MAE, MAPE, hoặc ngày dự báo bên trong JSON)
CREATE INDEX IF NOT EXISTS idx_marketresearch_forecast_result_gin ON reports_l1_marketresearchitem USING GIN (forecast_result);