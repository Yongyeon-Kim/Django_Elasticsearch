import csv
import sys
import glob
import os
from django.core.management.base import BaseCommand
from search_app.models import StandardDoc

csv.field_size_limit(sys.maxsize)  # 필드 길이 제한 해제

class Command(BaseCommand):
    help = 'Load all CSVs from data/output_KCS and data/output_KDS directories'

    def handle(self, *args, **options):
        folders = {
            'KCS': 'data/output_KCS/*.csv',
            'KDS': 'data/output_KDS/*.csv'
        }

        count = 0
        for code_type, pattern in folders.items():
            csv_files = glob.glob(pattern)
            for file_path in csv_files:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        code_value = row.get('code', '').strip()
                        if not code_value.isdigit():
                            continue
                        StandardDoc.objects.create(
                            code_type=code_type,
                            code=code_value,
                            name=row.get('name', '').strip(),
                            contents=row.get('contents', '').strip(),
                            name_en=row.get('name_en', '').strip(),
                            contents_en=row.get('contents_en', '').strip()
                        )
                        count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ 총 {count}건 색인 완료 (output_KCS, output_KDS 포함)"))
