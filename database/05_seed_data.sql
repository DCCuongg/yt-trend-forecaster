-- Mật khẩu mặc định là: pbkdf2_sha256 (Django hashed) hoặc plain demo
-- Hash bên dưới tương ứng với password: "AdminPassword123!"
INSERT INTO
    accounts_customuser (
        id,
        password,
        is_superuser,
        username,
        email,
        is_staff,
        is_active,
        role,
        prediction_quota,
        used_quota
    )
VALUES (
        1,
        'pbkdf2_sha256$720000$tJ92o...demo...$Yv0m3G+vHn4Ua5V0K8Z6nE=',
        TRUE,
        'admin',
        'admin@yttrend.local',
        TRUE,
        TRUE,
        'ADMIN',
        1000,
        0
    ),
    (
        2,
        'pbkdf2_sha256$720000$demo...creator...$Yv0m3G+vHn4Ua5V0K8Z6nE=',
        FALSE,
        'creator_demo',
        'creator@yttrend.local',
        FALSE,
        TRUE,
        'CREATOR',
        100,
        2
    ) ON CONFLICT (id) DO NOTHING;

-- Đặt lại giá trị serial sequence cho accounts_customuser
SELECT setval (
        'accounts_customuser_id_seq', (
            SELECT MAX(id)
            FROM accounts_customuser
        )
    );

-- Báo cáo mẫu
INSERT INTO
    reports_l1_trendreport (
        id,
        user_id,
        title,
        description,
        status
    )
VALUES (
        1,
        2,
        'Báo cáo xu hướng Gaming Q4/2026',
        'Phân tích từ khóa roblox, gta 5 trong 14 ngày tới',
        'READY'
    ) ON CONFLICT (id) DO NOTHING;

SELECT setval (
        'reports_l1_trendreport_id_seq', (
            SELECT MAX(id)
            FROM reports_l1_trendreport
        )
    );

-- Item nghiên cứu mẫu chứa dữ liệu JSONB
INSERT INTO reports_l1_marketresearchitem (
    id, report_id, topic_name, target_date, model_type, horizon_days, status, execution_duration_ms, forecast_result
) VALUES (
    1,
    1,
    'roblox',
    '2026-11-15',
    'LGBM_14DAY',
    14,
    'SUCCESS',
    420,
    '{
        "metrics": {"mae": 4.74, "mape": 17.09},
        "forecast_series": [
            {"date": "2026-11-16", "predicted_views": 18200000, "lower_bound": 16500000, "upper_bound": 19900000},
            {"date": "2026-11-17", "predicted_views": 19100000, "lower_bound": 17200000, "upper_bound": 21000000}
        ],
        "top_features": ["rolling_mean_7", "velocity_3d", "lag_1"]
    }'::jsonb
)
ON CONFLICT (id) DO NOTHING;

SELECT setval (
        'reports_l1_marketresearchitem_id_seq', (
            SELECT MAX(id)
            FROM reports_l1_marketresearchitem
        )
    );