import time
import requests
from django.conf import settings
from .local_predictor import LocalTrendPredictor

class InferenceRouter:
    """
    Router phân phối suy luận:
    - Chế độ LOCAL: Đọc model từ model_cache & chạy trực tiếp trên RAM máy chủ.
    - Chế độ REMOTE: Gửi payload sang Colab Worker API qua FastAPI/Cloudflare Tunnel.
    """
    def __init__(self):
        self.local_predictor = LocalTrendPredictor()

    def execute_forecast(self, topic_name: str, target_date_str: str, horizon_days: int) -> dict:
        start_time = time.time()
        mode = getattr(settings, "INFERENCE_MODE", "LOCAL")

        if mode == "REMOTE" and settings.COLAB_WORKER_URL:
            try:
                headers = {
                    "X-Worker-Key": settings.COLAB_WORKER_KEY,
                    "Content-Type": "application/json"
                }
                payload = {
                    "topic_name": topic_name,
                    "target_date": target_date_str,
                    "horizon_days": horizon_days
                }
                response = requests.post(
                    f"{settings.COLAB_WORKER_URL}/api/v1/predict", 
                    json=payload, 
                    headers=headers, 
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                # Nếu remote thất bại, tự động fallback sang local
                result = self.local_predictor.predict(topic_name, target_date_str, horizon_days)
                result["fallback_note"] = f"Remote failed ({str(e)}), fallen back to Local"
        else:
            result = self.local_predictor.predict(topic_name, target_date_str, horizon_days)

        duration_ms = int((time.time() - start_time) * 1000)
        return result, duration_ms