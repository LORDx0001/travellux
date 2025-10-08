from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='destinations/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"
    
    def __str__(self):
        return f"{self.name}, {self.country}"


class Tour(models.Model):
    TOUR_TYPES = [
        ('beach', 'Пляжный отдых'),
        ('cultural', 'Культурный туризм'),
        ('adventure', 'Приключенческий туризм'),
        ('city', 'Городской туризм'),
        ('nature', 'Природный туризм'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название тура")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Направление")
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES, verbose_name="Тип тура")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Старая цена")
    duration_days = models.IntegerField(verbose_name="Продолжительность (дни)")
    max_people = models.IntegerField(verbose_name="Максимум человек")
    image = models.ImageField(upload_to='tours/', verbose_name="Изображение")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'pk': self.pk})
    
    @property
    def has_discount(self):
        return self.old_price and self.old_price > self.price
    
    @property
    def discount_percent(self):
        if self.has_discount:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="Аватар")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"Профиль {self.user.username}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    people_count = models.IntegerField(verbose_name="Количество человек")
    start_date = models.DateField(verbose_name="Дата начала")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    notes = models.TextField(blank=True, verbose_name="Примечания")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Бронирование #{self.pk} - {self.tour.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    people_count = models.IntegerField(default=1, verbose_name="Количество человек")
    start_date = models.DateField(verbose_name="Дата начала")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        unique_together = ['user', 'tour']
    
    def __str__(self):
        return f"Корзина {self.user.username} - {self.tour.title}"
    
    @property
    def total_price(self):
        return self.tour.price * self.people_count


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тур")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ['tour', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв {self.user.username} - {self.tour.title}"
