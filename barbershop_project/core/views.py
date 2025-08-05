from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Master, Service, Order, Review
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, OrderForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш отзыв успешно отправлен! Спасибо!')
            return redirect(f"{reverse('thanks')}?source=review")
    else:
        form = ReviewForm()
    return render(request, 'core/review_form.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Ваша заявка успешно отправлена! Мы скоро свяжемся с вами.')
            return redirect(f"{reverse('thanks')}?source=order")
    else:
        form = OrderForm()
    return render(request, 'core/order_form.html', {'form': form})

def get_services(request):
    master_id = request.GET.get('master_id')
    services = Service.objects.filter(masters__id=master_id).values('id', 'name')
    return JsonResponse(list(services), safe=False)

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(is_published=True).order_by('-created_at')[:5]
        context['services'] = Service.objects.all()
        return context

@login_required
def orders_list(request):
    """
    Представление списка заказов (только для авторизованных пользователей).
    Поддерживает фильтрацию по поисковому запросу с настройкой полей поиска.
    """
    # Получаем параметры поиска из GET-запроса
    search_query = request.GET.get('search', '')  # Поисковая строка
    # Флажки выбора полей для поиска (по умолчанию только по имени)
    name_check = request.GET.get('name_check', 'on') == 'on'
    phone_check = request.GET.get('phone_check', 'off') == 'on'
    comment_check = request.GET.get('comment_check', 'off') == 'on'
    
    # Базовый запрос: все заказы, отсортированные по дате создания (новые сверху)
    orders = Order.objects.all().order_by('-date_created')
    
    # Применяем фильтрацию если есть поисковый запрос
    if search_query:
        # Создаем Q-объект для построения сложных запросов OR
        q_objects = Q()
        # Добавляем условия поиска в зависимости от выбранных чекбоксов
        if name_check:
            q_objects |= Q(client_name__icontains=search_query)  # Поиск по имени (без учета регистра)
        if phone_check:
            q_objects |= Q(phone__icontains=search_query)  # Поиск по телефону
        if comment_check:
            q_objects |= Q(comment__icontains=search_query)  # Поиск по комментарию
        
        # Применяем фильтр к queryset
        orders = orders.filter(q_objects)
    
    # Формируем контекст для передачи в шаблон
    context = {
        'orders': orders,
        'search_query': search_query,  # Сохраняем введенный запрос
        # Сохраняем состояния чекбоксов для отображения в форме
        'name_check': name_check,
        'phone_check': phone_check,
        'comment_check': comment_check,
    }
    return render(request, 'core/orders_list.html', context)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'  # Указываем, что параметр из URL называется order_id (а не pk по умолчанию)

class ThanksView(TemplateView):
    template_name = 'core/thanks.html'

class OrdersListView(LoginRequiredMixin, ListView):
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
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['name_check'] = self.request.GET.get('name_check', 'on') == 'on'
        context['phone_check'] = self.request.GET.get('phone_check', 'off') == 'on'
        context['comment_check'] = self.request.GET.get('comment_check', 'off') == 'on'
        return context

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш отзыв успешно отправлен! Спасибо!')
        return super().form_valid(form)
    
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваша заявка успешно отправлена! Мы скоро свяжемся с вами.')
        return super().form_valid(form)