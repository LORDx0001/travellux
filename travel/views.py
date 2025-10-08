from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Tour, Destination, Cart, Booking, UserProfile, Review
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm


def home(request):
    """Главная страница"""
    featured_tours = Tour.objects.filter(is_featured=True, is_active=True)[:6]
    destinations = Destination.objects.all()[:4]
    context = {
        'featured_tours': featured_tours,
        'destinations': destinations,
    }
    return render(request, 'travel/home.html', context)


def catalog(request):
    """Каталог туров"""
    tours = Tour.objects.filter(is_active=True)
    destinations = Destination.objects.all()
    
    # Фильтрация
    search = request.GET.get('search')
    destination_id = request.GET.get('destination')
    tour_type = request.GET.get('type')
    duration = request.GET.get('duration')
    
    if search:
        tours = tours.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(destination__name__icontains=search)
        )
    
    if destination_id:
        tours = tours.filter(destination_id=destination_id)
    
    if tour_type:
        tours = tours.filter(tour_type=tour_type)
    
    if duration:
        if duration == 'short':
            tours = tours.filter(duration_days__lte=7)
        elif duration == 'medium':
            tours = tours.filter(duration_days__range=(8, 14))
        elif duration == 'long':
            tours = tours.filter(duration_days__gte=15)
    
    context = {
        'tours': tours,
        'destinations': destinations,
        'tour_types': Tour.TOUR_TYPES,
        'current_search': search or '',
        'current_destination': destination_id,
        'current_type': tour_type,
        'current_duration': duration,
    }
    return render(request, 'travel/catalog.html', context)


def tour_detail(request, pk):
    """Детальная страница тура"""
    tour = get_object_or_404(Tour, pk=pk, is_active=True)
    reviews = tour.reviews.all()
    related_tours = Tour.objects.filter(
        destination=tour.destination, 
        is_active=True
    ).exclude(pk=tour.pk)[:3]
    
    context = {
        'tour': tour,
        'reviews': reviews,
        'related_tours': related_tours,
    }
    return render(request, 'travel/tour_detail.html', context)


@login_required
def cart(request):
    """Корзина"""
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    discount = int(total * 0.05)  # 5% скидка
    final_total = total - discount
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    }
    return render(request, 'travel/cart.html', context)


@login_required
def add_to_cart(request, tour_id):
    """Добавить в корзину"""
    tour = get_object_or_404(Tour, pk=tour_id, is_active=True)
    
    if request.method == 'POST':
        people_count = int(request.POST.get('people_count', 1))
        start_date = request.POST.get('start_date')
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            tour=tour,
            defaults={
                'people_count': people_count,
                'start_date': start_date,
            }
        )
        
        if not created:
            cart_item.people_count += people_count
            cart_item.save()
        
        messages.success(request, 'Тур добавлен в корзину!')
        return redirect('cart')
    
    return redirect('tour_detail', pk=tour_id)


@login_required
@login_required
def remove_from_cart(request, cart_id):
    """Удалить из корзины"""
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Тур удален из корзины!')
    return redirect('cart')


@login_required
def clear_cart(request):
    """Очистить корзину"""
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Корзина очищена!')
    return redirect('cart')


def auth_view(request):
    """Авторизация"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            print(f"Данные входа: {request.POST}")  # Отладка
            print(f"Форма входа валидна: {login_form.is_valid()}")  # Отладка
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'Добро пожаловать!')
                print(f"Пользователь {user.username} вошел в систему")  # Отладка
                
                # Перенаправление на страницу, с которой пришел пользователь
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('profile')
            else:
                print(f"Ошибки входа: {login_form.errors}")  # Отладка
                messages.error(request, 'Неверное имя пользователя или пароль')
        
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            print(f"Данные регистрации: {request.POST}")  # Отладка
            print(f"Форма регистрации валидна: {register_form.is_valid()}")  # Отладка
            if register_form.is_valid():
                user = register_form.save()
                print(f"Создан пользователь: {user.username}")  # Отладка
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                
                # Перенаправление на страницу, с которой пришел пользователь
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('profile')
            else:
                print(f"Ошибки регистрации: {register_form.errors}")  # Отладка
                messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    
    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'travel/simple_auth.html', context)


@login_required
def profile(request):
    """Личный кабинет"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'bookings': bookings,
    }
    return render(request, 'travel/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        # Проверяем, нужно ли удалить аватар
        if request.POST.get('remove_avatar'):
            if profile.avatar:
                profile.avatar.delete()
            profile.avatar = None
            profile.save()
            messages.success(request, 'Фото профиля удалено!')
            return redirect('edit_profile')
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'travel/edit_profile.html', context)


def logout_view(request):
    """Выход"""
    logout(request)
    messages.success(request, 'Вы вышли из системы!')
    return redirect('home')


def register_view(request):
    """Регистрация"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        print(f"Данные регистрации: {request.POST}")  # Отладка
        print(f"Форма регистрации валидна: {register_form.is_valid()}")  # Отладка
        if register_form.is_valid():
            user = register_form.save()
            print(f"Создан пользователь: {user.username}")  # Отладка
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
        else:
            print(f"Ошибки регистрации: {register_form.errors}")  # Отладка
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    
    return render(request, 'travel/register.html')


def about(request):
    """О нас"""
    context = {
        'company_info': {
            'name': 'TravelUX',
            'description': 'Мы создаем незабываемые путешествия по всему миру',
            'experience_years': 10,
            'tours_count': 500,
            'happy_clients': 10000,
        }
    }
    return render(request, 'travel/about.html', context)


def test_404(request):
    """Тестовая страница для проверки 404"""
    from django.shortcuts import render
    return render(request, '404.html', status=404)


def test_500(request):
    """Тестовая страница для проверки 500"""
    from django.shortcuts import render
    return render(request, '500.html', status=500)


def test_403(request):
    """Тестовая страница для проверки 403"""
    from django.shortcuts import render
    return render(request, '403.html', status=403)


def test_errors(request):
    """Страница для тестирования всех ошибок"""
    return render(request, 'travel/test_errors.html')
