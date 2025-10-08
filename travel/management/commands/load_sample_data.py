from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from decimal import Decimal
import requests
from io import BytesIO
from travel.models import Destination, Tour


class Command(BaseCommand):
    help = 'Загружает тестовые данные для туров и направлений'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю загрузку тестовых данных...')
        
        # Создаем направления
        destinations_data = [
            {
                'name': 'Париж',
                'country': 'Франция',
                'description': 'Город любви и романтики, известный Эйфелевой башней, Лувром и уютными кафе.',
                'image_url': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=800&h=600&fit=crop'
            },
            {
                'name': 'Рим',
                'country': 'Италия',
                'description': 'Вечный город с богатой историей, Колизей, Ватикан и восхитительная итальянская кухня.',
                'image_url': 'https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=800&h=600&fit=crop'
            },
            {
                'name': 'Токио',
                'country': 'Япония',
                'description': 'Современный мегаполис с древними традициями, технологии будущего и уникальная культура.',
                'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&h=600&fit=crop'
            },
            {
                'name': 'Нью-Йорк',
                'country': 'США',
                'description': 'Город, который никогда не спит. Небоскребы, Бродвей, Центральный парк и энергия мегаполиса.',
                'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800&h=600&fit=crop'
            },
            {
                'name': 'Дубай',
                'country': 'ОАЭ',
                'description': 'Современный оазис в пустыне с роскошными отелями, торговыми центрами и пляжами.',
                'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&h=600&fit=crop'
            },
            {
                'name': 'Бали',
                'country': 'Индонезия',
                'description': 'Тропический рай с красивыми пляжами, рисовыми террасами и духовной атмосферой.',
                'image_url': 'https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800&h=600&fit=crop'
            },
            {
                'name': 'Лондон',
                'country': 'Великобритания',
                'description': 'Столица с богатой историей, Биг-Бен, Букингемский дворец и традиционные пабы.',
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&h=600&fit=crop'
            },
            {
                'name': 'Барселона',
                'country': 'Испания',
                'description': 'Город Гауди с уникальной архитектурой, пляжами и живой атмосферой.',
                'image_url': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=800&h=600&fit=crop'
            }
        ]

        destinations = {}
        for dest_data in destinations_data:
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                country=dest_data['country'],
                defaults={
                    'description': dest_data['description']
                }
            )
            
            if created:
                # Загружаем изображение
                try:
                    response = requests.get(dest_data['image_url'])
                    if response.status_code == 200:
                        image_content = ContentFile(response.content)
                        destination.image.save(
                            f"{dest_data['name'].lower().replace(' ', '_')}.jpg",
                            image_content,
                            save=True
                        )
                        self.stdout.write(f'✓ Создано направление: {destination.name}')
                    else:
                        self.stdout.write(f'⚠ Не удалось загрузить изображение для {destination.name}')
                except Exception as e:
                    self.stdout.write(f'⚠ Ошибка загрузки изображения для {destination.name}: {e}')
            else:
                self.stdout.write(f'→ Направление {destination.name} уже существует')
            
            destinations[dest_data['name']] = destination

        # Создаем туры
        tours_data = [
            {
                'title': 'Романтический уикенд в Париже',
                'destination': 'Париж',
                'tour_type': 'cultural',
                'description': 'Проведите незабываемые выходные в самом романтичном городе мира. Посетите Эйфелеву башню, прогуляйтесь по Монмартру, насладитесь ужином в уютном ресторанчике.',
                'price': Decimal('89900'),
                'old_price': Decimal('99900'),
                'duration_days': 3,
                'max_people': 2,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=800&h=600&fit=crop'
            },
            {
                'title': 'Гастрономическое путешествие по Италии',
                'destination': 'Рим',
                'tour_type': 'cultural',
                'description': 'Откройте для себя секреты итальянской кухни. Мастер-классы от шеф-поваров, дегустации вин, посещение местных рынков и традиционных ресторанов.',
                'price': Decimal('120000'),
                'old_price': Decimal('135000'),
                'duration_days': 7,
                'max_people': 12,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?w=800&h=600&fit=crop'
            },
            {
                'title': 'Технологии будущего: Токио',
                'destination': 'Токио',
                'tour_type': 'city',
                'description': 'Погрузитесь в мир высоких технологий и древних традиций. Посетите роботов-ресторан, храмы, рынок Цукидзи и районы Сибуя и Харадзюку.',
                'price': Decimal('150000'),
                'duration_days': 10,
                'max_people': 15,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800&h=600&fit=crop'
            },
            {
                'title': 'Нью-Йорк: город контрастов',
                'destination': 'Нью-Йорк',
                'tour_type': 'city',
                'description': 'Экскурсии по Манхэттену, посещение музеев, шоу на Бродвее, прогулка по Центральному парку и покупки на 5-й авеню.',
                'price': Decimal('180000'),
                'old_price': Decimal('200000'),
                'duration_days': 8,
                'max_people': 20,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1485871981521-5b1fd3805b6d?w=800&h=600&fit=crop'
            },
            {
                'title': 'Роскошь Дубая',
                'destination': 'Дубай',
                'tour_type': 'beach',
                'description': 'Отдых в роскошных отелях, посещение Бурдж-Халифа, сафари в пустыне, шопинг в торговых центрах и релакс на пляжах.',
                'price': Decimal('140000'),
                'duration_days': 6,
                'max_people': 10,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?w=800&h=600&fit=crop'
            },
            {
                'title': 'Йога-ретрит на Бали',
                'destination': 'Бали',
                'tour_type': 'nature',
                'description': 'Духовное путешествие с ежедневными занятиями йогой, медитацией, посещением храмов и знакомством с балийской культурой.',
                'price': Decimal('95000'),
                'old_price': Decimal('110000'),
                'duration_days': 14,
                'max_people': 8,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1552055568-3a47b6ecad03?w=800&h=600&fit=crop'
            },
            {
                'title': 'Классическая Англия',
                'destination': 'Лондон',
                'tour_type': 'cultural',
                'description': 'Традиционное английское путешествие: Биг-Бен, Тауэр, Букингемский дворец, чаепитие и поездка в Стоунхендж.',
                'price': Decimal('125000'),
                'duration_days': 5,
                'max_people': 16,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1520986606214-8b456906c813?w=800&h=600&fit=crop'
            },
            {
                'title': 'Архитектурные шедевры Барселоны',
                'destination': 'Барселона',
                'tour_type': 'cultural',
                'description': 'Исследуйте творения Гауди: Саграда Фамилия, Парк Гуэль, Дом Бальо. Прогулки по Готическому кварталу и пляжам.',
                'price': Decimal('105000'),
                'old_price': Decimal('115000'),
                'duration_days': 6,
                'max_people': 12,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800&h=600&fit=crop'
            },
            {
                'title': 'Пляжный отдых в Дубае',
                'destination': 'Дубай',
                'tour_type': 'beach',
                'description': 'Расслабляющий отдых на лучших пляжах Персидского залива с водными видами спорта и спа-процедурами.',
                'price': Decimal('110000'),
                'duration_days': 7,
                'max_people': 8,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop'
            },
            {
                'title': 'Приключения в Токио',
                'destination': 'Токио',
                'tour_type': 'adventure',
                'description': 'Активный отдых: восхождение на Фудзи, картинг по улицам Токио, посещение тематических парков и ночной жизни.',
                'price': Decimal('165000'),
                'duration_days': 12,
                'max_people': 6,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1551818255-e6e10975cd17?w=800&h=600&fit=crop'
            }
        ]

        for tour_data in tours_data:
            destination = destinations.get(tour_data['destination'])
            if not destination:
                self.stdout.write(f'⚠ Направление {tour_data["destination"]} не найдено для тура {tour_data["title"]}')
                continue

            tour, created = Tour.objects.get_or_create(
                title=tour_data['title'],
                defaults={
                    'destination': destination,
                    'tour_type': tour_data['tour_type'],
                    'description': tour_data['description'],
                    'price': tour_data['price'],
                    'old_price': tour_data.get('old_price'),
                    'duration_days': tour_data['duration_days'],
                    'max_people': tour_data['max_people'],
                    'is_featured': tour_data['is_featured'],
                }
            )
            
            if created:
                # Загружаем изображение
                try:
                    response = requests.get(tour_data['image_url'])
                    if response.status_code == 200:
                        image_content = ContentFile(response.content)
                        tour.image.save(
                            f"{tour_data['title'].lower().replace(' ', '_').replace(':', '')}.jpg",
                            image_content,
                            save=True
                        )
                        self.stdout.write(f'✓ Создан тур: {tour.title}')
                    else:
                        self.stdout.write(f'⚠ Не удалось загрузить изображение для {tour.title}')
                except Exception as e:
                    self.stdout.write(f'⚠ Ошибка загрузки изображения для {tour.title}: {e}')
            else:
                self.stdout.write(f'→ Тур {tour.title} уже существует')

        self.stdout.write(self.style.SUCCESS('Загрузка тестовых данных завершена!'))
        
        # Статистика
        destinations_count = Destination.objects.count()
        tours_count = Tour.objects.count()
        featured_tours_count = Tour.objects.filter(is_featured=True).count()
        
        self.stdout.write(f'\n📊 Статистика:')
        self.stdout.write(f'   • Направления: {destinations_count}')
        self.stdout.write(f'   • Туры: {tours_count}')
        self.stdout.write(f'   • Рекомендуемые туры: {featured_tours_count}')