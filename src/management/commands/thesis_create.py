from django.core.management.base import BaseCommand

from src.models.summary.thesis import Thesis


class Command(BaseCommand):
    help = '샘플 논문 요약 데이터 생성'

    def add_arguments(self, parser):
        parser.add_argument('-n', type=int, help='생성할 개수')

    def handle(self, *args, **options):
        num = options['n']

        for i in range(num):
            Thesis.objects.create(
                user_id=1,
                url=f'url_{i+1}',
                content=f'content_{i+1}'
            )
