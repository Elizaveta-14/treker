from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from habit.models import Habit
from users.models import User


class HabitTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='TEST@mail.ru')
        self.habit = Habit.objects.create(title='Test', action='TESTaction', time='20:00', time_to_do=100,
                                          reward='TESTreward', owner=self.user, is_public=True)
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """ Тест списка всех HABIT в БД """

        url = reverse('habit:habit-list')
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {'count': 1, 'next': None, 'previous': None, 'results':
                [{'id': 4, 'title': 'Test', 'is_pleasant': False, 'place': None, 'time': '20:00:00',
                  'action': 'TESTaction', 'period': 1, 'reward': 'TESTreward', 'time_to_do': 100, 'is_public': True,
                  'send_indicator': 1, 'related_habit': None}]}
        )

        # Сверяем ожидаемое количество Habit в БД
        self.assertEqual(
            Habit.objects.count(),
            1
        )

    def test_habit_retrieve(self):
        """ Тест детальной информации обьекта """

        url = reverse('habit:habit-detail', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {'id': 5, 'title': 'Test', 'is_pleasant': False, 'place': None, 'time': '20:00:00',
             'action': 'TESTaction', 'period': 1, 'reward': 'TESTreward', 'time_to_do': 100, 'is_public': True,
             'send_indicator': 1, 'related_habit': None}
        )

    def test_habit_create(self):
        """ Тестирование создание обьекта HABIT """

        data = {
            'title': 'TestCREATE',
            'action': 'TESTaction',
            'time': '20:00:00',
            'time_to_do': 100,
            'reward': 'TESTreward'
        }
        response = self.client.post(
            '/habit/',
            data=data
        )

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Сверяем ожидаемое количество Habit в БД
        self.assertEqual(
            Habit.objects.count(),
            2
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'TestCREATE', 'is_pleasant': None, 'place': None, 'time': '20:00:00',
             'action': 'TESTaction', 'period': 1, 'reward': 'TESTreward', 'time_to_do': 100, 'is_public': None,
             'send_indicator': 1, 'related_habit': None}

        )

    def test_habit_update(self):
        """ Тестирование обновление обьекта HABIT """

        url = reverse("habit:habit-detail", args=(self.habit.pk,))

        data = {
            'title': 'TestUPDATE',
            'action': 'TESTUPDATE',
            'time': '19:00:00',
            'time_to_do': 50,
            'reward': 'TESTrewardUPDATE'
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Сверяем ожидаемое количество Habit в БД
        self.assertEqual(
            Habit.objects.count(),
            1
        )

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json()["title"], 'TestUPDATE')

    def test_habit_delete(self):
        """ Тестирование удаление обьекта HABIT """

        url = reverse("habit:habit-detail", args=(self.habit.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Сверяем ожидаемое количество Habit в БД
        self.assertEqual(
            Habit.objects.count(),
            0
        )
