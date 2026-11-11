import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Lệnh chặn tiến trình cho tới khi PostgreSQL sẵn sàng kết nối"""
    def handle(self, *args, **options):
        self.stdout.write("Đang chờ cơ sở dữ liệu PostgreSQL khởi động...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("PostgreSQL chưa sẵn sàng, thử lại sau 1 giây...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("PostgreSQL đã sẵn sàng kết nối!"))