from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from core.models import Order
from core.telegram import send_telegram_message
import logging

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=Order.services.through)
def notify_about_new_order(sender, instance, action, **kwargs):
    if action == 'post_add':
        try:
            message = (
                f"🎉 *Новый заказ!*\n"
                f"🔹 *Клиент:* {instance.client_name}\n"
                f"📞 *Телефон:* {instance.phone}\n"
                f"🧔 *Мастер:* {instance.master.name if instance.master else 'Не указан'}\n"
                f"📅 *Дата записи:* {instance.appointment_date}\n"
                f"🔧 *Услуги:* {', '.join(s.name for s in instance.services.all())}"
            )
            if not send_telegram_message(message):
                logger.error("Не удалось отправить сообщение в Telegram")
        except Exception as e:
            logger.error(f"Ошибка в сигнале: {e}")