from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrendReportViewSet, MarketResearchItemViewSet

router = DefaultRouter()
router.register(r"list", TrendReportViewSet, basename="report")
router.register(r"research", MarketResearchItemViewSet, basename="market-research")

urlpatterns = [
    path("", include(router.urls)),
]