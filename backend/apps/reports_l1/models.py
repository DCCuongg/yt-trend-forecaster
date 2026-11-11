from django.db import models
from django.conf import settings

class TrendReport(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Bản nháp"
        READY = "READY", "Đã hoàn thành"
        ARCHIVED = "ARCHIVED", "Lưu trữ"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trend_reports")
    title = models.CharField(max_length=255, help_text="Tên báo cáo phân tích")
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class MarketResearchItem(models.Model):
    """
    Đại diện cho 1 lệnh nghiên cứu thị trường / 1 phiên chạy model trong Báo cáo.
    """
    class ModelChoice(models.TextChoices):
        LGBM_14DAY = "LGBM_14DAY", "LightGBM 14 Ngày"
        PROPHET_QUARTER = "PROPHET_QUARTER", "Prophet 1 Quý (90 Ngày)"
        LSTM_YEAR = "LSTM_YEAR", "LSTM Chuỗi Thời Gian 1 Năm (365 Ngày)"

    class ExecutionStatus(models.TextChoices):
        PENDING = "PENDING", "Đang chờ xử lý"
        PROCESSING = "PROCESSING", "Đang chạy mô hình"
        SUCCESS = "SUCCESS", "Thành công"
        FAILED = "FAILED", "Thất bại"

    report = models.ForeignKey(TrendReport, on_delete=models.CASCADE, related_name="research_items")
    topic_name = models.CharField(max_length=150, help_text="Chủ đề/từ khóa dự đoán (ví dụ: Gaming, roblox)")
    target_date = models.DateField(help_text="Ngày mốc bắt đầu dự báo (YYYY-MM-DD)")
    model_type = models.CharField(
        max_length=30, 
        choices=ModelChoice.choices, 
        default=ModelChoice.LGBM_14DAY
    )
    horizon_days = models.PositiveIntegerField(default=14, help_text="Số ngày dự đoán tương lai")
    
    status = models.CharField(
        max_length=20, 
        choices=ExecutionStatus.choices, 
        default=ExecutionStatus.PENDING
    )
    
    # Lưu trữ kết quả JSON nguyên bản từ Model trong PostgreSQL JSONField (jsonb)
    forecast_result = models.JSONField(
        blank=True, 
        null=True, 
        help_text="Chứa series dự báo, confidence bounds, metrics (MAE/MAPE), features snapshot"
    )
    error_message = models.TextField(blank=True, null=True)

    execution_duration_ms = models.PositiveIntegerField(default=0, help_text="Thời gian chạy model tính theo ms")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Research [{self.topic_name} - {self.model_type}] in Report #{self.report_id}"