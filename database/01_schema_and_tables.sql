-- Kích hoạt extension hỗ trợ tìm kiếm UUID và JSONB nâng cao
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- 1. Bảng User (accounts_customuser)
CREATE TABLE IF NOT EXISTS accounts_customuser (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) NOT NULL DEFAULT 'CREATOR',
    prediction_quota INT NOT NULL DEFAULT 100,
    used_quota INT NOT NULL DEFAULT 0,
    avatar_url VARCHAR(500) NULL
);

-- 2. Bảng Báo cáo Xu hướng (reports_l1_trendreport)
CREATE TABLE IF NOT EXISTS reports_l1_trendreport (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trendreport_user FOREIGN KEY (user_id) REFERENCES accounts_customuser (id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- 3. Bảng Lệnh nghiên cứu / Chạy Model (reports_l1_marketresearchitem)
CREATE TABLE IF NOT EXISTS reports_l1_marketresearchitem (
    id BIGSERIAL PRIMARY KEY,
    report_id BIGINT NOT NULL,
    topic_name VARCHAR(150) NOT NULL,
    target_date DATE NOT NULL,
    model_type VARCHAR(30) NOT NULL DEFAULT 'LGBM_14DAY',
    horizon_days INT NOT NULL DEFAULT 14,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    forecast_result JSONB NULL,
    error_message TEXT NULL,
    execution_duration_ms INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_marketresearch_report FOREIGN KEY (report_id) REFERENCES reports_l1_trendreport (id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);