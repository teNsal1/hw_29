import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
import django
django.setup()

from core.models import Master, Service, Order, Review
from django.utils import timezone
import random

# Создание мастеров (с обновлением ID)
masters_data = [
    Master(
        name=f"Мастер {i}",
        photo="",
        phone=f"+7{random.randint(9000000000, 9999999999)}",
        address=f"Адрес {i}",
        experience=random.randint(1, 10),
        is_active=True
    ) for i in range(1, 6)
]
Master.objects.bulk_create(masters_data)
masters = list(Master.objects.all())  # Получаем объекты с актуальными ID

# Создание услуг
services = [
    Service(
        name=f"Услуга {i}",
        description=f"Описание услуги {i}",
        price=random.randint(500, 3000),
        duration=random.randint(30, 120),
        is_popular=random.choice([True, False]),
        image=""
    ) for i in range(1, 11)
]
Service.objects.bulk_create(services)

# Создание заказов (синтаксис исправлен)
statuses = ['not_approved', 'approved', 'in_progress', 'completed', 'cancelled']
for i in range(1, 16):
    order = Order.objects.create(  # Добавлена закрывающая скобка для create()
        client_name=f"Клиент {i}",
        phone=f"+7{random.randint(9000000000, 9999999999)}",
        comment=f"Комментарий к заказу {i}",
        status=random.choice(statuses),
        master=random.choice(masters),
        appointment_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30))
    )  # Закрывающая скобка для всего create()

    # Добавление услуг к заказу
    num_services = random.randint(1, 4)
    order.services.set(random.sample(list(Service.objects.all()), num_services))

# Создание отзывов (с актуальными мастерами)
for i in range(1, 11):
    Review.objects.create(
        text=f"Отличный сервис! {i}",
        client_name=f"Клиент {i}",
        master=random.choice(masters),  # Используем список с ID
        rating=random.randint(3, 5),
        is_published=True
    )

print("Тестовые данные успешно созданы!")