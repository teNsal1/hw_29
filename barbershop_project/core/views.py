from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Master, Service, Order, Review
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm, OrderForm
from django.urls import reverse
from django.contrib import messages

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

def landing(request):
    """
    Представление главной страницы (лендинга).
    Отображает активных мастеров, опубликованные отзывы и все услуги.
    """
    # Получаем активных мастеров
    masters = Master.objects.filter(is_active=True)
    # 5 последних опубликованных отзывов (сортировка по дате создания)
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:5]
    # Все доступные услуги
    services = Service.objects.all()
    
    # Формируем контекст для шаблона
    context = {
        'masters': masters,
        'services': services,
        'reviews': reviews,  # Передаем отзывы в шаблон
    }
    return render(request, 'landing.html', context)

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

@login_required
def order_detail(request, order_id):
    """
    Детальное представление заказа (только для авторизованных пользователей).
    Отображает информацию о конкретном заказе по его ID.
    """
    # Получаем объект заказа или 404 ошибку если не найден
    order = get_object_or_404(Order, id=order_id)
    # Передаем заказ в контекст шаблона
    context = {'order': order}
    return render(request, 'core/order_detail.html', context)

def thanks(request):
    return render(request, 'core/thanks.html')