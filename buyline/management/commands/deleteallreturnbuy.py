from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from buyline.models import ReturnProduct


class Command(BaseCommand):
    help = 'Delete all query on return buy.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hour',
            action='store_true',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        self.objects = ReturnProduct.objects.all()

        if options['hour']:
            end_time = datetime.now() - timedelta(hours=1)
            end_time = make_aware(end_time)
            self.objects = self.objects.filter(return_product_at__gte=end_time)

        self.objects.delete()
