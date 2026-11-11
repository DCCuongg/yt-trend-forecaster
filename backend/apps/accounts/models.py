from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Sinh viên"
        CREATOR = "CREATOR", "Nhà sáng tạo nội dung"
        ADMIN = "ADMIN", "Quản trị viên"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CREATOR)
    prediction_quota = models.PositiveIntegerField(
        default=100, 
        help_text="Số lượt gọi suy luận dự báo được phép thực hiện"
    )
    used_quota = models.PositiveIntegerField(default=0)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)

    def has_quota(self) -> bool:
        return self.used_quota < self.prediction_quota

    def consume_quota(self):
        self.used_quota += 1
        self.save(update_fields=["used_quota"])

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"