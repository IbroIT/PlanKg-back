from django.core.management.base import BaseCommand
from services.models import Category


class Command(BaseCommand):
    help = 'Load event planning categories for Plan.kg'

    def handle(self, *args, **kwargs):
        # Clear existing categories
        Category.objects.all().delete()
        
        categories_data = [
            # 1. Рестораны
            {
                'translations': {'ru': 'Рестораны', 'en': 'Restaurants', 'kg': 'Ресторандар'},
                'slug': 'restaurants-main',
                'icon': '🍽️',
                'order': 1,
                'children': [
                    {'translations': {'ru': 'Рестораны', 'en': 'Restaurants', 'kg': 'Ресторандар'}, 'slug': 'restaurants', 'icon': '🏛️'},
                    {'translations': {'ru': 'Кейтеринг', 'en': 'Catering', 'kg': 'Кейтеринг'}, 'slug': 'catering', 'icon': '🍴'},
                    {'translations': {'ru': 'Компании (все включено)', 'en': 'All-inclusive Companies', 'kg': 'Компаниялар (баары кошулган)'}, 'slug': 'all-inclusive', 'icon': '🎪'},
                    {'translations': {'ru': 'Индивидуально', 'en': 'Individual', 'kg': 'Жеке'}, 'slug': 'individual-catering', 'icon': '👤'},
                ]
            },
            
            # 2. Персонал
            {
                'translations': {'ru': 'Персонал', 'en': 'Staff', 'kg': 'Кызматкерлер'},
                'slug': 'staff',
                'icon': '👨‍🍳',
                'order': 2,
                'children': [
                    {'translations': {'ru': 'Повар', 'en': 'Chef', 'kg': 'Ашпоз'}, 'slug': 'chef', 'icon': '👨‍🍳'},
                    {'translations': {'ru': 'Бармен', 'en': 'Bartender', 'kg': 'Бармен'}, 'slug': 'bartender', 'icon': '🍸'},
                    {'translations': {'ru': 'Официант', 'en': 'Waiter', 'kg': 'Официант'}, 'slug': 'waiter', 'icon': '🤵'},
                    {'translations': {'ru': 'Уборка', 'en': 'Cleaning', 'kg': 'Тазалоо'}, 'slug': 'cleaning', 'icon': '🧹'},
                    {'translations': {'ru': 'Посудомойка', 'en': 'Dishwasher', 'kg': 'Идиш жуугуч'}, 'slug': 'dishwasher', 'icon': '🍽️'},
                ]
            },
            
            # 3. Развлечения
            {
                'translations': {'ru': 'Развлечения', 'en': 'Entertainment', 'kg': 'Көңүл ачуу'},
                'slug': 'entertainment',
                'icon': '🎭',
                'order': 3,
                'children': [
                    {'translations': {'ru': 'Ведущий/Тамада', 'en': 'Host/MC', 'kg': 'Алып баруучу/Тамада'}, 'slug': 'host-mc', 'icon': '🎤'},
                    {'translations': {'ru': 'Шоу-программы', 'en': 'Show Programs', 'kg': 'Шоу программалар'}, 'slug': 'show-programs', 'icon': '🎪'},
                    {'translations': {'ru': 'Певцы', 'en': 'Singers', 'kg': 'Ырчылар'}, 'slug': 'singers', 'icon': '🎵'},
                    {'translations': {'ru': 'Танцоры', 'en': 'Dancers', 'kg': 'Бийчилер'}, 'slug': 'dancers', 'icon': '💃'},
                    {'translations': {'ru': 'Аниматоры', 'en': 'Animators', 'kg': 'Аниматорлор'}, 'slug': 'animators', 'icon': '🤡'},
                    {'translations': {'ru': 'Оркестр', 'en': 'Orchestra', 'kg': 'Оркестр'}, 'slug': 'orchestra', 'icon': '🎻'},
                    {'translations': {'ru': 'Фокусник', 'en': 'Magician', 'kg': 'Фокусчу'}, 'slug': 'magician', 'icon': '🎩'},
                ]
            },
            
            # 4. Организация
            {
                'translations': {'ru': 'Организация мероприятий', 'en': 'Event Planning', 'kg': 'Иш-чараларды уюштуруу'},
                'slug': 'event-planning',
                'icon': '📋',
                'order': 4,
                'children': [
                    {'translations': {'ru': 'Организаторы мероприятий', 'en': 'Event Organizers', 'kg': 'Иш-чаралардын уюштуруучулары'}, 'slug': 'event-organizers', 'icon': '📅'},
                    {'translations': {'ru': 'Праздничное оформление', 'en': 'Holiday Decoration', 'kg': 'Майрамдык оформление'}, 'slug': 'holiday-decoration', 'icon': '🎉'},
                ]
            },
            
            # 5. Декор и оформление
            {
                'translations': {'ru': 'Декор и оформление', 'en': 'Decor & Design', 'kg': 'Декор жана оформление'},
                'slug': 'decor-design',
                'icon': '🎨',
                'order': 5,
                'children': [
                    {'translations': {'ru': 'Декор', 'en': 'Decor', 'kg': 'Декор'}, 'slug': 'decor', 'icon': '✨'},
                    {'translations': {'ru': 'Фото стенды', 'en': 'Photo Booths', 'kg': 'Фото стенддери'}, 'slug': 'photo-booths', 'icon': '📸'},
                    {'translations': {'ru': 'Шарики', 'en': 'Balloons', 'kg': 'Шарлар'}, 'slug': 'balloons', 'icon': '🎈'},
                ]
            },
            
            # 6. Приглашения
            {
                'translations': {'ru': 'Приглашения', 'en': 'Invitations', 'kg': 'Чакыруулар'},
                'slug': 'invitations',
                'icon': '💌',
                'order': 6,
                'children': [
                    {'translations': {'ru': 'Пригласительные', 'en': 'Invitation Cards', 'kg': 'Чакыруу карттары'}, 'slug': 'invitation-cards', 'icon': '💌'},
                    {'translations': {'ru': 'Открытки', 'en': 'Cards', 'kg': 'Карттар'}, 'slug': 'cards', 'icon': '🎁'},
                    {'translations': {'ru': 'Сайт-приглашения', 'en': 'Website Invitations', 'kg': 'Сайт-чакыруулар'}, 'slug': 'website-invitations', 'icon': '💻'},
                ]
            },
            
            # 7. Фото/Видео
            {
                'translations': {'ru': 'Фото и Видео', 'en': 'Photo & Video', 'kg': 'Фото жана Видео'},
                'slug': 'photo-video',
                'icon': '📷',
                'order': 7,
                'children': [
                    {'translations': {'ru': 'Студии', 'en': 'Studios', 'kg': 'Студиялар'}, 'slug': 'studios', 'icon': '🏢'},
                    {'translations': {'ru': 'Фотограф', 'en': 'Photographer', 'kg': 'Фотограф'}, 'slug': 'photographer', 'icon': '📷'},
                    {'translations': {'ru': 'Видеограф', 'en': 'Videographer', 'kg': 'Видеограф'}, 'slug': 'videographer', 'icon': '🎥'},
                ]
            },
            
            # 8. Свадебные платья
            {
                'translations': {'ru': 'Свадебные платья', 'en': 'Wedding Dresses', 'kg': 'Үйлөнүү көйнөктөрү'},
                'slug': 'wedding-dresses',
                'icon': '👗',
                'order': 8,
                'children': [
                    {'translations': {'ru': 'Купить', 'en': 'Buy', 'kg': 'Сатып алуу'}, 'slug': 'buy-dresses', 'icon': '🛍️'},
                    {'translations': {'ru': 'Аренда', 'en': 'Rent', 'kg': 'Ижарага алуу'}, 'slug': 'rent-dresses', 'icon': '👗'},
                ]
            },
            
            # 9. Салон красоты
            {
                'translations': {'ru': 'Салон красоты', 'en': 'Beauty Salon', 'kg': 'Сулуулук салону'},
                'slug': 'beauty-salon',
                'icon': '💅',
                'order': 9,
                'children': [
                    {'translations': {'ru': 'Прическа', 'en': 'Hairstyle', 'kg': 'Чач жасоо'}, 'slug': 'hairstyle', 'icon': '💇'},
                    {'translations': {'ru': 'Макияж', 'en': 'Makeup', 'kg': 'Макияж'}, 'slug': 'makeup', 'icon': '💄'},
                    {'translations': {'ru': 'Маникюр/Педикюр', 'en': 'Manicure/Pedicure', 'kg': 'Маникюр/Педикюр'}, 'slug': 'manicure-pedicure', 'icon': '💅'},
                ]
            },
            
            # 10. Цветы
            {
                'translations': {'ru': 'Цветы', 'en': 'Flowers', 'kg': 'Гүлдөр'},
                'slug': 'flowers',
                'icon': '💐',
                'order': 10,
                'children': [
                    {'translations': {'ru': 'Букет невесты', 'en': 'Bridal Bouquet', 'kg': 'Келиндин букети'}, 'slug': 'bridal-bouquet', 'icon': '💐'},
                    {'translations': {'ru': 'Цветы для оформления', 'en': 'Decoration Flowers', 'kg': 'Оформлениеге гүлдөр'}, 'slug': 'decoration-flowers', 'icon': '🌸'},
                    {'translations': {'ru': 'Цветы', 'en': 'Flowers', 'kg': 'Гүлдөр'}, 'slug': 'flowers-general', 'icon': '�'},
                ]
            },
            
            # 11. Ювелирные изделия
            {
                'translations': {'ru': 'Ювелирные изделия', 'en': 'Jewelry', 'kg': 'Зергерлик буюмдар'},
                'slug': 'jewelry',
                'icon': '💍',
                'order': 11,
                'children': [
                    {'translations': {'ru': 'Ювелирные изделия', 'en': 'Jewelry', 'kg': 'Зергерлик буюмдар'}, 'slug': 'jewelry-items', 'icon': '💎'},
                ]
            },
        ]
        
        # Create categories
        for cat_data in categories_data:
            children = cat_data.pop('children', [])
            parent = Category.objects.create(**cat_data)
            self.stdout.write(self.style.SUCCESS(f'Created parent category: {parent.get_translation("ru")}'))
            
            # Create subcategories
            for i, child_data in enumerate(children, start=1):
                child_data['parent'] = parent
                child_data['order'] = i
                child = Category.objects.create(**child_data)
                self.stdout.write(self.style.SUCCESS(f'  - Created subcategory: {child.get_translation("ru")}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All event categories loaded successfully!'))
