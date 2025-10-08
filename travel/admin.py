from django.contrib import admin
from .models import Destination, Tour, UserProfile, Booking, Cart, Review


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    list_filter = ('country', 'created_at')
    search_fields = ('name', 'country')


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'tour_type', 'price', 'duration_days', 'is_featured', 'is_active')
    list_filter = ('tour_type', 'is_featured', 'is_active', 'destination__country')
    search_fields = ('title', 'description', 'destination__name')
    list_editable = ('is_featured', 'is_active', 'price')
    readonly_fields = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'people_count', 'start_date', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'created_at')
    search_fields = ('user__username', 'tour__title')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'people_count', 'start_date', 'created_at')
    search_fields = ('user__username', 'tour__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('tour__title', 'user__username', 'comment')
