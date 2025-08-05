from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('review/create/', views.ReviewCreateView.as_view(), name='create_review'),
    path('order/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('get_services/', views.get_services, name='get_services'),
]