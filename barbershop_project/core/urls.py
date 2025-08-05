from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('review/create/', views.create_review, name='create_review'),
    path('order/create/', views.create_order, name='create_order'),
    path('thanks/', views.thanks, name='thanks'),
    path('get_services/', views.get_services, name='get_services'),
]