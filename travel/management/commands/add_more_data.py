from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from decimal import Decimal
import requests
from travel.models import Destination, Tour


class Command(BaseCommand):
    help = 'Добавляет дополнительные туры и направления'

    def handle(self, *args, **options):
        self.stdout.write('Добавляю дополнительные туры...')
        
        # Создаем дополнительные направления
        additional_destinations = [
            {
                'name': 'Стамбул',
                'country': 'Турция',
                'description': 'Город на стыке Европы и Азии с богатой историей, великолепными мечетями и восточным колоритом.',
                'image_url': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&h=600&fit=crop'
            },
            {
                'name': 'Санторини',
                'country': 'Греция',
                'description': 'Романтический остров с белоснежными домиками, голубыми куполами и потрясающими закатами.',
                'image_url': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&h=600&fit=crop'
            },
            {
                'name': 'Прага',
                'country': 'Чехия',
                'description': 'Сказочный город с готической архитектурой, старинными мостами и богемной атмосферой.',
                'image_url': 'https://images.unsplash.com/photo-1541849546-216549ae216d?w=800&h=600&fit=crop'
            }
        ]

        destinations = {}
        # Получаем существующие направления
        for dest in Destination.objects.all():
            destinations[dest.name] = dest

        # Добавляем новые направления
        for dest_data in additional_destinations:
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                country=dest_data['country'],
                defaults={
                    'description': dest_data['description']
                }
            )
            
            if created:
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
                except Exception as e:
                    self.stdout.write(f'⚠ Ошибка загрузки изображения для {destination.name}: {e}')
            
            destinations[dest_data['name']] = destination

        # Дополнительные туры
        additional_tours = [
            {
                'title': 'Мистический Стамбул',
                'destination': 'Стамбул',
                'tour_type': 'cultural',
                'description': 'Погрузитесь в атмосферу древнего Константинополя. Голубая мечеть, Айя-София, Гранд-базар и круиз по Босфору.',
                'price': Decimal('85000'),
                'old_price': Decimal('95000'),
                'duration_days': 5,
                'max_people': 14,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1548503301-b3a3b8c1b6b8?w=800&h=600&fit=crop'
            },
            {
                'title': 'Романтика Санторини',
                'destination': 'Санторини',
                'tour_type': 'beach',
                'description': 'Незабываемый медовый месяц на самом романтичном острове Греции. Закаты в Ие, винные дегустации и спа.',
                'price': Decimal('135000'),
                'duration_days': 7,
                'max_people': 6,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=800&h=600&fit=crop'
            },
            {
                'title': 'Сказочная Прага',
                'destination': 'Прага',
                'tour_type': 'cultural',
                'description': 'Прогулки по средневековому городу, Пражский град, Карлов мост и дегустация знаменитого чешского пива.',
                'price': Decimal('75000'),
                'old_price': Decimal('85000'),
                'duration_days': 4,
                'max_people': 18,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1513805959324-96eb66ca8713?w=800&h=600&fit=crop'
            },
            {
                'title': 'Экстремальные приключения в Дубае',
                'destination': 'Дубай',
                'tour_type': 'adventure',
                'description': 'Банджи-джампинг, полеты на вертолете, катание на багги по пустыне и прыжки с парашютом.',
                'price': Decimal('200000'),
                'duration_days': 5,
                'max_people': 8,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1587891237815-15fd8e4827e4?w=800&h=600&fit=crop'
            },
            {
                'title': 'Семейный отдых в Париже',
                'destination': 'Париж',
                'tour_type': 'cultural',
                'description': 'Идеальный семейный тур: Диснейленд, зоопарк, Эйфелева башня и круизы по Сене.',
                'price': Decimal('115000'),
                'duration_days': 6,
                'max_people': 20,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1471623432079-b009d30b6729?w=800&h=600&fit=crop'
            },
            {
                'title': 'Тропический рай Бали',
                'destination': 'Бали',
                'tour_type': 'beach',
                'description': 'Расслабляющий пляжный отдых с массажами, серфингом и посещением храмов.',
                'price': Decimal('125000'),
                'old_price': Decimal('140000'),
                'duration_days': 10,
                'max_people': 12,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop'
            },
            {
                'title': 'Музеи и галереи Лондона',
                'destination': 'Лондон',
                'tour_type': 'cultural',
                'description': 'Культурное погружение: Британский музей, Тейт Модерн, Национальная галерея и театры Вест-Энда.',
                'price': Decimal('145000'),
                'duration_days': 8,
                'max_people': 15,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1529655683826-aba9b3e77383?w=800&h=600&fit=crop'
            },
            {
                'title': 'Фламенко и тапас в Барселоне',
                'destination': 'Барселона',
                'tour_type': 'cultural',
                'description': 'Почувствуйте дух Испании: уроки фламенко, дегустация тапас, посещение футбольного стадиона Камп Ноу.',
                'price': Decimal('98000'),
                'duration_days': 5,
                'max_people': 16,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1570654639102-bdd95efeca7a?w=800&h=600&fit=crop'
            }
        ]

        for tour_data in additional_tours:
            destination = destinations.get(tour_data['destination'])
            if not destination:
                self.stdout.write(f'⚠ Направление {tour_data["destination"]} не найдено')
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
                except Exception as e:
                    self.stdout.write(f'⚠ Ошибка загрузки изображения для {tour.title}: {e}')
            else:
                self.stdout.write(f'→ Тур {tour.title} уже существует')

        self.stdout.write(self.style.SUCCESS('Дополнительные данные загружены!'))
        
        # Финальная статистика
        destinations_count = Destination.objects.count()
        tours_count = Tour.objects.count()
        featured_tours_count = Tour.objects.filter(is_featured=True).count()
        
        self.stdout.write(f'\n📊 Финальная статистика:')
        self.stdout.write(f'   • Направления: {destinations_count}')
        self.stdout.write(f'   • Туры: {tours_count}')
        self.stdout.write(f'   • Рекомендуемые туры: {featured_tours_count}')
        
        # Статистика по типам туров
        self.stdout.write(f'\n🏷️ Туры по типам:')
        for tour_type, name in Tour.TOUR_TYPES:
            count = Tour.objects.filter(tour_type=tour_type).count()
            self.stdout.write(f'   • {name}: {count}')
        
        # Статистика по странам
        self.stdout.write(f'\n🌍 Направления по странам:')
        countries = Destination.objects.values_list('country', flat=True).distinct()
        for country in countries:
            count = Destination.objects.filter(country=country).count()
            self.stdout.write(f'   • {country}: {count}')