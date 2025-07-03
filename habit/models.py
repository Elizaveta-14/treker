from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Habit(models.Model):
    """ Модель Привычки """

    # METHOD_CHOICE = [
    #
    #     ('daily', 'Ежедневная'),
    #     ('weekly', 'Еженедельная'),
    #     ('monthly', 'Ежемесячная')
    # ]

    title = models.CharField(max_length=100, verbose_name="Название")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Владелец")
    is_pleasant = models.BooleanField(default=False, blank=True, null=True, verbose_name="Флаг приятности")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная приятная привычка",
        blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=100, blank=True, null=True, verbose_name="Действие")
    period = models.PositiveIntegerField(default=1, verbose_name="Переодичность")
    reward = models.CharField(max_length=100, blank=True, null=True, verbose_name="Вознаграждение")
    time_to_do = models.PositiveIntegerField(default=120, blank=True, null=True, verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, blank=True, null=True, verbose_name="Публичность")
    send_indicator = models.PositiveIntegerField(default=1, verbose_name="Индикатор отправки")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.title if self.title else self.action})"

    def clean(self):
        """ Валидация полей """

        # Проверка на вознаграждения в приятной привычке
        if self.is_pleasant and self.reward:
            raise ValidationError(
                "Нельзя в приятной привычки указывать вознаграждение."
            )
        # Проверка на переодичность привычки - не реже один раз в 7 дней
        if self.period > 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )
        # Проверка на превышения лимита выполнения в 120 секунд.
        if self.time_to_do > 120:
            raise ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )

    def save(self, *args, **kwargs):
        """ Сохраняем изменения после валидаций """

        self.clean()
        super().save(*args, **kwargs)
