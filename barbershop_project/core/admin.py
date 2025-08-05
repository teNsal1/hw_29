from django.contrib import admin
from django.utils import timezone
from .models import Master, Service, Order, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class DateFilter(admin.SimpleListFilter):
    title = 'Дата создания'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Сегодня'),
            ('week', 'За неделю'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_at__date=timezone.now().date())
        if self.value() == 'week':
            return queryset.filter(created_at__date__gte=timezone.now().date() - timezone.timedelta(days=7))
        return queryset

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone')
    inlines = [ReviewInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'appointment_date', 'master')
    list_filter = ('status', 'master')
    search_fields = ('client_name', 'phone')
    date_hierarchy = 'appointment_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = (DateFilter, 'rating', 'is_published', 'master')
    search_fields = ('client_name', 'text')
    date_hierarchy = 'created_at'
    actions = ['publish_reviews', 'unpublish_reviews']

    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
    publish_reviews.short_description = "Опубликовать выбранные отзывы"

    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_reviews.short_description = "Снять с публикации выбранные отзывы"