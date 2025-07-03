from celery import shared_task

from habit.models import Habit
from habit.services import send_telegram
from django.utils import timezone


@shared_task
def send_message_to_user():
    """ Проверка на отправление привычки и отправка, если не была отправлена  """

    habits = Habit.objects.all()
    time_now = timezone.localtime().strftime("%H:%M")

    for habit in habits:
        if habit.send_indicator == 1:
            if habit.time.strftime("%H:%M") == time_now:

                text = (f"Необходимо выполнить: {habit.action.lower()}.\nМесто выполнения: {habit.place.lower()}.\n"
                        f"Продолжиленость выполнения: {habit.time_to_do} секунд.")
                try:

                    send_telegram(habit.owner.tg_chat_id, text)
                    habit.send_indicator = 0
                    habit.save()

                except Exception as e:
                    print(f"Ошибка в отправке письма. Ошибка: {e}")