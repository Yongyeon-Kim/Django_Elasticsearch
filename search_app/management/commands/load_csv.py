import csv
import sys
from django.core.management.base import BaseCommand
from search_app.models import StandardDoc

csv.field_size_limit(sys.maxsize)  # 필드 길이 제한 해제

class Command(BaseCommand):
    help = 'Load data from csv_KCS.csv and csv_KDS.csv'

    def handle(self, *args, **options):
        for filename, code_type in [('csv_KCS.csv', 'KCS'), ('csv_KDS.csv', 'KDS')]:
            with open(f'/code/{filename}', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    code_value = row.get('code', '').strip()
                    if not code_value.isdigit():
                        continue
                    if not code_type:
                        continue
                    StandardDoc.objects.create(
                        code_type=code_type,
                        code=code_value,
                        name=row.get('name', '').strip(),
                        contents=row.get('contents', '').strip()
                    )
        self.stdout.write(self.style.SUCCESS("CSV 데이터 로드 완료"))
