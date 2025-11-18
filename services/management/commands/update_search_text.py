"""
Management command to update search_text field for all services
Usage: python manage.py update_search_text
"""
from django.core.management.base import BaseCommand
from services.models import Service


class Command(BaseCommand):
    help = 'Update search_text field for all services'

    def handle(self, *args, **kwargs):
        services = Service.objects.all()
        updated_count = 0

        for service in services:
            old_search_text = service.search_text
            service.update_search_text()
            if service.search_text != old_search_text:
                service.save(update_fields=['search_text'])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Updated search_text for {updated_count} services')
        )