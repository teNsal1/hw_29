from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Master, Service, Order, Review
from .forms import ReviewForm, OrderForm


class LandingView(TemplateView):
    """
    Главная страница сайта. Отображает активных мастеров, опубликованные отзывы и услуги.
    """
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['services'] = Service.objects.all()
        return context


class OrdersListView(LoginRequiredMixin, ListView):
    """
    Список заказов с возможностью фильтрации по поисковому запросу.
    Доступен только для авторизованных пользователей.
    """
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            q_objects = Q()
            if self.request.GET.get('name_check', 'on') == 'on':
                q_objects |= Q(client_name__icontains=search_query)
            if self.request.GET.get('phone_check', 'off') == 'on':
                q_objects |= Q(phone__icontains=search_query)
            if self.request.GET.get('comment_check', 'off') == 'on':
                q_objects |= Q(comment__icontains=search_query)
            queryset = queryset.filter(q_objects)
        
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляет в контекст параметры поиска для отображения в форме."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['name_check'] = self.request.GET.get('name_check', 'on') == 'on'
        context['phone_check'] = self.request.GET.get('phone_check', 'off') == 'on'
        context['comment_check'] = self.request.GET.get('comment_check', 'off') == 'on'
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Детальная информация о заказе.
    Доступна только для авторизованных пользователей.
    """
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'


class ReviewCreateView(CreateView):
    """
    Создание нового отзыва. После успешного создания перенаправляет на страницу благодарности.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш отзыв успешно отправлен! Спасибо!')
        return super().form_valid(form)


class OrderCreateView(CreateView):
    """
    Создание новой заявки. После успешного создания перенаправляет на страницу благодарности.
    """
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваша заявка успешно отправлена! Мы скоро свяжемся с вами.')
        return super().form_valid(form)


class ThanksView(TemplateView):
    """Страница благодарности после отправки формы."""
    template_name = 'core/thanks.html'


def get_services(request):
    """
    Возвращает JSON-список услуг для выбранного мастера.
    Используется для динамической подгрузки в формах.
    """
    master_id = request.GET.get('master_id')
    services = Service.objects.filter(masters__id=master_id).values('id', 'name')
    return JsonResponse(list(services), safe=False)