from unittest import TestCase

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class HabitTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="TEST@mail.ru")
        self.client.force_authenticate(user=self.user)

    def test_user_update(self):
        """Тестирование обновление обьекта USER"""

        url = reverse("users:user-detail", args=(self.user.pk,))

        data = {
            "email": "TestUPDATE@mail.ru",
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем ожидаемое количество User в БД
        self.assertEqual(User.objects.count(), 1)

        # Сверяем данные с ожидаемыми
        self.assertEqual(response.json()["email"], "TestUPDATE@mail.ru")

    def test_user_list(self):
        """Тест списка всех USER в БД"""

        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            [
                {
                    "id": self.user.id,
                    "email": "TEST@mail.ru",
                    "first_name": None,
                    "last_name": None,
                    "phone": None,
                    "country": None,
                    "photo": None,
                }
            ],
        )

        # Сверяем ожидаемое количество User в БД
        self.assertEqual(User.objects.count(), 1)

    def test_user_retrieve(self):
        """Тест детальной информации обьекта"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем статус кода
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            data,
            {
                "id": self.user.id,
                "email": "TEST@mail.ru",
                "first_name": None,
                "last_name": None,
                "phone": None,
                "country": None,
                "photo": None,
            },
        )

    def test_user_create(self):
        """Тестирование создание обьекта USER"""

        data = {
            "email": "TestCREATE@mail.ru",
            "country": "TESTcountry",
            "time": "00:00",
            "tg_chat_id": 331431412,
            "phone": "TESTphone",
            "password": 1111,
        }
        response = self.client.post("/user/", data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Сверяем ожидаемое количество Habit в БД
        self.assertEqual(User.objects.count(), 2)

        # Сверяем данные с ожидаемыми
        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "email": "TestCREATE@mail.ru",
                "first_name": None,
                "last_name": None,
                "phone": "TESTphone",
                "country": "TESTcountry",
                "photo": None,
            },
        )

    def test_user_delete(self):
        """Тестирование удаление обьекта USER"""

        url = reverse("users:user-detail", args=(self.user.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Сверяем ожидаемое количество User в БД
        self.assertEqual(User.objects.count(), 0)


class CreateSuperuserCommandTest(TestCase):
    def test_create_superuser(self):
        # Вызов команды
        call_command("csu")

        # Проверка, что пользователь создан
        self.assertEqual(User.objects.count(), 1)

        # Получение созданного пользователя
        user = User.objects.first()

        # Проверка атрибутов пользователя
        self.assertEqual(user.email, "user@mail.ru")
        self.assertTrue(user.check_password("1234"))
        self.assertTrue(user.is_active)
