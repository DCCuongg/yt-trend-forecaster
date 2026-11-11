-- 1. Stored Procedure trừ quota dự báo (có transaction lock chống race condition)
CREATE OR REPLACE PROCEDURE sp_consume_prediction_quota(
    IN p_user_id BIGINT,
    OUT p_success BOOLEAN,
    OUT p_remaining_quota INT,
    OUT p_message TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_prediction_quota INT;
    v_used_quota INT;
BEGIN
    -- Khóa dòng dữ liệu của user để xử lý concurrency an toàn
    SELECT prediction_quota, used_quota 
    INTO v_prediction_quota, v_used_quota
    FROM accounts_customuser
    WHERE id = p_user_id
    FOR UPDATE;

    IF NOT FOUND THEN
        p_success := FALSE;
        p_remaining_quota := 0;
        p_message := 'Người dùng không tồn tại';
        RETURN;
    END IF;

    IF v_used_quota >= v_prediction_quota THEN
        p_success := FALSE;
        p_remaining_quota := 0;
        p_message := 'Hạn mức dự báo đã cạn (Quota Exceeded)';
        RETURN;
    END IF;

    -- Tăng hạn mức sử dụng lên 1
    UPDATE accounts_customuser
    SET used_quota = used_quota + 1
    WHERE id = p_user_id;

    p_success := TRUE;
    p_remaining_quota := v_prediction_quota - (v_used_quota + 1);
    p_message := 'Trừ hạn ngạch thành công';
END;
$$;

-- 2. Stored Procedure cấp lại quota định kỳ cho người dùng
CREATE OR REPLACE PROCEDURE sp_reset_quota(
    IN p_role_target VARCHAR(20),
    IN p_new_quota INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE accounts_customuser
    SET prediction_quota = p_new_quota,
        used_quota = 0
    WHERE role = p_role_target;
    
    COMMIT;
END;
$$;