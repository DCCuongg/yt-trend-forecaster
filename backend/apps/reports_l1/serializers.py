from rest_framework import serializers
from .models import TrendReport, MarketResearchItem

class MarketResearchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketResearchItem
        fields = (
            "id", "report", "topic_name", "target_date", "model_type", 
            "horizon_days", "status", "forecast_result", "error_message", 
            "execution_duration_ms", "created_at"
        )
        read_only_fields = ("id", "status", "forecast_result", "error_message", "execution_duration_ms", "created_at")

    def validate(self, attrs):
        model_type = attrs.get("model_type", MarketResearchItem.ModelChoice.LGBM_14DAY)
        # Tự động gán horizon_days tương ứng với lựa chọn model nếu người dùng không truyền
        if not attrs.get("horizon_days"):
            if model_type == MarketResearchItem.ModelChoice.LGBM_14DAY:
                attrs["horizon_days"] = 14
            elif model_type == MarketResearchItem.ModelChoice.PROPHET_QUARTER:
                attrs["horizon_days"] = 90
            elif model_type == MarketResearchItem.ModelChoice.LSTM_YEAR:
                attrs["horizon_days"] = 365
        return attrs


class TrendReportSerializer(serializers.ModelSerializer):
    research_items = MarketResearchItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = TrendReport
        fields = ("id", "title", "description", "status", "created_at", "updated_at", "item_count", "research_items")
        read_only_fields = ("id", "created_at", "updated_at", "item_count")

    def get_item_count(self, obj) -> int:
        return obj.research_items.count()