from django.core.management.base import BaseCommand
from ...utils import generate_products

class Command(BaseCommand):
    help = "Generate dummy data for books"

    def handle(self, *args, **kwargs):
        generate_products(50)
        print("complete")