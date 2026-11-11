from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.permissions import IsOwner
from .models import TrendReport, MarketResearchItem
from .serializers import TrendReportSerializer, MarketResearchItemSerializer
from .services.inference_router import InferenceRouter

class TrendReportViewSet(viewsets.ModelViewSet):
    """
    CRUD Báo cáo của Người dùng.
    Mỗi người dùng chỉ được xem và quản lý báo cáo của chính họ.
    """
    serializer_class = TrendReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return TrendReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MarketResearchItemViewSet(viewsets.ModelViewSet):
    """
    Quản lý và thực thi các lệnh nghiên cứu/dự báo bên trong từng Báo cáo.
    """
    serializer_class = MarketResearchItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MarketResearchItem.objects.filter(report__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_quota():
            return Response(
                {"detail": "Hạn mức (Quota) dự báo của bạn đã hết. Vui lòng liên hệ quản trị viên."},
                status=status.HTTP_403_FORBIDDEN
            )

        report_id = request.data.get("report")
        report = get_object_or_404(TrendReport, id=report_id, user=user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 1. Lưu bản ghi ở trạng thái PROCESSING
        research_item = serializer.save(status=MarketResearchItem.ExecutionStatus.PROCESSING)

        # 2. Khởi tạo Router và thực thi suy luận
        router = InferenceRouter()
        try:
            result_json, duration_ms = router.execute_forecast(
                topic_name=research_item.topic_name,
                target_date_str=str(research_item.target_date),
                horizon_days=research_item.horizon_days
            )
            research_item.forecast_result = result_json
            research_item.execution_duration_ms = duration_ms
            research_item.status = MarketResearchItem.ExecutionStatus.SUCCESS
            research_item.save()

            # Trừ hạn mức gọi của tài khoản
            user.consume_quota()
            
            # Cập nhật trạng thái báo cáo nếu cần
            if report.status == TrendReport.Status.DRAFT:
                report.status = TrendReport.Status.READY
                report.save(update_fields=["status"])

        except Exception as e:
            research_item.status = MarketResearchItem.ExecutionStatus.FAILED
            research_item.error_message = str(e)
            research_item.save()
            return Response(
                {
                    "detail": "Quá trình suy luận thất bại.",
                    "error": str(e),
                    "item": MarketResearchItemSerializer(research_item).data
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(MarketResearchItemSerializer(research_item).data, status=status.HTTP_201_CREATED)