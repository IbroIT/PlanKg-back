"""
Management command to load initial categories
Usage: python manage.py load_categories
"""
from django.core.management.base import BaseCommand
from services.models import Category


class Command(BaseCommand):
    help = 'Load initial service categories'

    def handle(self, *args, **kwargs):
        categories_data = [
            {
                'slug': 'hairdresser',
                'icon': '💇',
                'translations': {
                    'ru': 'Парикмахер',
                    'en': 'Hairdresser',
                    'kg': 'Чач кыркуучу'
                }
            },
            {
                'slug': 'electrician',
                'icon': '⚡',
                'translations': {
                    'ru': 'Электрик',
                    'en': 'Electrician',
                    'kg': 'Электрик'
                }
            },
            {
                'slug': 'plumber',
                'icon': '🔧',
                'translations': {
                    'ru': 'Сантехник',
                    'en': 'Plumber',
                    'kg': 'Сантехник'
                }
            },
            {
                'slug': 'photographer',
                'icon': '📷',
                'translations': {
                    'ru': 'Фотограф',
                    'en': 'Photographer',
                    'kg': 'Фотограф'
                }
            },
            {
                'slug': 'tutor',
                'icon': '📚',
                'translations': {
                    'ru': 'Репетитор',
                    'en': 'Tutor',
                    'kg': 'Мугалим'
                }
            },
            {
                'slug': 'cleaner',
                'icon': '🧹',
                'translations': {
                    'ru': 'Уборка',
                    'en': 'Cleaning',
                    'kg': 'Тазалоо'
                }
            },
            {
                'slug': 'builder',
                'icon': '🏗️',
                'translations': {
                    'ru': 'Строитель',
                    'en': 'Builder',
                    'kg': 'Куруучу'
                }
            },
            {
                'slug': 'mechanic',
                'icon': '🔩',
                'translations': {
                    'ru': 'Автомеханик',
                    'en': 'Mechanic',
                    'kg': 'Механик'
                }
            },
            {
                'slug': 'designer',
                'icon': '🎨',
                'translations': {
                    'ru': 'Дизайнер',
                    'en': 'Designer',
                    'kg': 'Дизайнер'
                }
            },
            {
                'slug': 'cook',
                'icon': '👨‍🍳',
                'translations': {
                    'ru': 'Повар',
                    'en': 'Cook',
                    'kg': 'Ашпоз'
                }
            },
            {
                'slug': 'lawyer',
                'icon': '⚖️',
                'translations': {
                    'ru': 'Юрист',
                    'en': 'Lawyer',
                    'kg': 'Юрист'
                }
            },
            {
                'slug': 'translator',
                'icon': '🗣️',
                'translations': {
                    'ru': 'Переводчик',
                    'en': 'Translator',
                    'kg': 'Которуучу'
                }
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'icon': cat_data['icon'],
                    'translations': cat_data['translations']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {cat_data["translations"]["ru"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {cat_data["translations"]["ru"]}')
                )

        self.stdout.write(self.style.SUCCESS('\nAll categories loaded successfully!'))
