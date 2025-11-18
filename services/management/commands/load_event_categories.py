from django.core.management.base import BaseCommand
from services.models import Category


class Command(BaseCommand):
    help = 'Load event planning categories for Plan.kg'

    def handle(self, *args, **kwargs):
        # Clear existing categories
        Category.objects.all().delete()
        
        categories_data = [
            # 1. Фотографы
            {
                'translations': {'ru': 'Фотографы', 'en': 'Photographers', 'kg': 'Фотографтар'},
                'slug': 'photographers',
                'icon': '📸',
                'order': 1,
            },
            
            # 2. Видеооператоры
            {
                'translations': {'ru': 'Видеооператоры', 'en': 'Videographers', 'kg': 'Видеооператорлор'},
                'slug': 'videographers',
                'icon': '🎥',
                'order': 2,
            },
            
            # 3. Ведущие / Тамада
            {
                'translations': {'ru': 'Ведущие / Тамада', 'en': 'Hosts / Toastmasters', 'kg': 'Алып баруучулар / Тамадалар'},
                'slug': 'hosts-toastmasters',
                'icon': '🎤',
                'order': 3,
            },
            
            # 4. Залы / Рестораны / Площадки
            {
                'translations': {'ru': 'Залы / Рестораны / Площадки', 'en': 'Venues / Restaurants / Halls', 'kg': 'Залдар / Ресторандар / Аянтчалар'},
                'slug': 'venues-restaurants-halls',
                'icon': '🏛️',
                'order': 4,
            },
            
            # 5. Флористы / Декораторы
            {
                'translations': {'ru': 'Флористы / Декораторы', 'en': 'Florists / Decorators', 'kg': 'Флористтер / Декораторлор'},
                'slug': 'florists-decorators',
                'icon': '💐',
                'order': 5,
            },
            
            # 6. Кейтеринг
            {
                'translations': {'ru': 'Кейтеринг', 'en': 'Catering', 'kg': 'Кейтеринг'},
                'slug': 'catering',
                'icon': '🍽️',
                'order': 6,
            },
            
            # 7. Музыканты / Ди-джеи / Группы
            {
                'translations': {'ru': 'Музыканты / Ди-джеи / Группы', 'en': 'Musicians / DJs / Bands', 'kg': 'Музыканттар / Ди-джеилер / Группалар'},
                'slug': 'musicians-djs-bands',
                'icon': '🎵',
                'order': 7,
            },
            
            # 8. Артисты / Шоу-программа
            {
                'translations': {'ru': 'Артисты / Шоу-программа', 'en': 'Artists / Show Programs', 'kg': 'Артистер / Шоу программалар'},
                'slug': 'artists-show-programs',
                'icon': '🎭',
                'order': 8,
            },
            
            # 9. Организаторы / Event-агентства
            {
                'translations': {'ru': 'Организаторы / Event-агентства', 'en': 'Event Organizers / Agencies', 'kg': 'Уюштуруучулар / Event агенттиктери'},
                'slug': 'event-organizers-agencies',
                'icon': '📋',
                'order': 9,
            },
            
            # 10. Транспорт (авто, лимузины, автобусы)
            {
                'translations': {'ru': 'Транспорт (авто, лимузины, автобусы)', 'en': 'Transportation (cars, limousines, buses)', 'kg': 'Транспорт (авто, лимузиндер, автобус)'},
                'slug': 'transportation',
                'icon': '🚗',
                'order': 10,
            },
            
            # 11. Стилисты / Визажисты / Парикмахеры
            {
                'translations': {'ru': 'Стилисты / Визажисты / Парикмахеры', 'en': 'Stylists / Makeup Artists / Hairdressers', 'kg': 'Стилисттер / Визажисттер / Парикмахерлер'},
                'slug': 'stylists-makeup-hairdressers',
                'icon': '💄',
                'order': 11,
            },
            
            # 12. Пекарни / Торты / Десерты
            {
                'translations': {'ru': 'Пекарни / Торты / Десерты', 'en': 'Bakeries / Cakes / Desserts', 'kg': 'Пекарнялар / Торттор / Десерттер'},
                'slug': 'bakeries-cakes-desserts',
                'icon': '🍰',
                'order': 12,
            },
            
            # 13. Фото-зоны / Оборудование / Реквизит
            {
                'translations': {'ru': 'Фото-зоны / Оборудование / Реквизит', 'en': 'Photo Zones / Equipment / Props', 'kg': 'Фото-зоналар / Жабдуулар / Реквизит'},
                'slug': 'photo-zones-equipment-props',
                'icon': '📷',
                'order': 13,
            },
            
            # 14. Официанты / Персонал на мероприятие
            {
                'translations': {'ru': 'Официанты / Персонал на мероприятие', 'en': 'Waiters / Event Staff', 'kg': 'Официанттар / Иш-чара персоналы'},
                'slug': 'waiters-event-staff',
                'icon': '🤵',
                'order': 14,
            },
            
            # 15. Охрана
            {
                'translations': {'ru': 'Охрана', 'en': 'Security', 'kg': 'Камсыздоо'},
                'slug': 'security',
                'icon': '🛡️',
                'order': 15,
            },
            
            # 16. Аниматоры (детские мероприятия)
            {
                'translations': {'ru': 'Аниматоры (детские мероприятия)', 'en': 'Animators (children\'s events)', 'kg': 'Аниматорлор (балдар иш-чаралары)'},
                'slug': 'animators-children-events',
                'icon': '🤡',
                'order': 16,
            },
            
            # 17. Освещение / Звук / Сцена
            {
                'translations': {'ru': 'Освещение / Звук / Сцена', 'en': 'Lighting / Sound / Stage', 'kg': 'Жарык / Үн / Сахна'},
                'slug': 'lighting-sound-stage',
                'icon': '🎛️',
                'order': 17,
            },
        ]
        
        # Create categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'translations': cat_data['translations'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.get_translation("ru")}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.get_translation("ru")}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All event categories loaded successfully!'))
