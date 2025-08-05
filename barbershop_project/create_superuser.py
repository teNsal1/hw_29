import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    User.objects.create_superuser(
        username='rinat',
        email='tensal@bk.ru',
        password='rinat'
    )
    print("Суперпользователь успешно создан!")
except Exception as e:
    print(f"Ошибка: {e}")