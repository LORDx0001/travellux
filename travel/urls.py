from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:tour_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    # Тестовые страницы ошибок (только для разработки)
    path('test-errors/', views.test_errors, name='test_errors'),
    path('test/404/', views.test_404, name='test_404'),
    path('test/500/', views.test_500, name='test_500'),
    path('test/403/', views.test_403, name='test_403'),
]