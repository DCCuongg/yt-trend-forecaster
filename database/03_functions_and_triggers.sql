-- 1. Hàm tự động cập nhật updated_at
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Gắn trigger cho bảng reports_l1_trendreport
DROP TRIGGER IF EXISTS set_timestamp_trendreport ON reports_l1_trendreport;

CREATE TRIGGER set_timestamp_trendreport
    BEFORE UPDATE ON reports_l1_trendreport
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- Gắn trigger cho bảng reports_l1_marketresearchitem
DROP TRIGGER IF EXISTS set_timestamp_marketresearchitem ON reports_l1_marketresearchitem;

CREATE TRIGGER set_timestamp_marketresearchitem
    BEFORE UPDATE ON reports_l1_marketresearchitem
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- 2. Trigger tự động chuyển trạng thái TrendReport sang READY khi tất cả items chạy SUCCESS
CREATE OR REPLACE FUNCTION check_and_update_report_status()
RETURNS TRIGGER AS $$
DECLARE
    pending_or_running_count INT;
BEGIN
    -- Kiểm tra xem còn item nào trong report chưa hoàn tất không
    SELECT COUNT(*) INTO pending_or_running_count
    FROM reports_l1_marketresearchitem
    WHERE report_id = NEW.report_id AND status IN ('PENDING', 'PROCESSING');

    IF pending_or_running_count = 0 THEN
        UPDATE reports_l1_trendreport
        SET status = 'READY', updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.report_id AND status = 'DRAFT';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_sync_report_status ON reports_l1_marketresearchitem;

CREATE TRIGGER trg_sync_report_status
    AFTER UPDATE OF status ON reports_l1_marketresearchitem
    FOR EACH ROW
    WHEN (NEW.status IN ('SUCCESS', 'FAILED'))
    EXECUTE FUNCTION check_and_update_report_status();