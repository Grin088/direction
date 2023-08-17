import json

from datetime import date
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError
from ref_books.models import RefBook, RefBookVersion, RefBookElement


class RefBooksModelTest(TestCase):
    fixtures = ['fixtures/001_user.json']

    @classmethod
    def setUpClass(cls):
        """Функция для создания записей в db"""
        super().setUpClass()
        cls.ref_book_1 = RefBook.objects.create(
            code='1',
            name='Специальности медицинских работников',
            description=''
        )

        cls.ref_book_2 = RefBook.objects.create(
            code='2',
            name='Должности медицинских работников',
            description=''
        )

        cls.ref_book_version_1 = RefBookVersion.objects.create(
            ref_book_id=cls.ref_book_1,
            version='1.0',
            start_date=date(2023, 8, 2)
        )

        cls.ref_book_version_2 = RefBookVersion.objects.create(
            ref_book_id=cls.ref_book_1,
            version='1.1',
            start_date=date(2023, 8, 10)
        )

        cls.ref_book_version_3 = RefBookVersion.objects.create(
            ref_book_id=cls.ref_book_2,
            version='1.0',
            start_date=date(2023, 8, 11)
        )

        cls.ref_book_element_1 = RefBookElement.objects.create(
            ref_book_version_id=cls.ref_book_version_2,
            code='1',
            value='Терапевт'
        )

        cls.ref_book_element_2 = RefBookElement.objects.create(
            ref_book_version_id=cls.ref_book_version_2,
            code='2',
            value='Травматолог'
        )

        cls.ref_book_element_3 = RefBookElement.objects.create(
            ref_book_version_id=cls.ref_book_version_2,
            code='3',
            value='Хирург'
        )

        cls.ref_book_element_3 = RefBookElement.objects.create(
            ref_book_version_id=cls.ref_book_version_3,
            code='1',
            value='Заведующий'
        )

    @classmethod
    def tearDownClass(cls):
        """Метод для удаления объектов после теста"""
        RefBookElement.objects.all().delete()
        RefBookVersion.objects.all().delete()
        RefBook.objects.all().delete()
        super().tearDownClass()

    def test_duplicate_direction_code(self):
        """
        Тест для проверки создания справочника с уникальным кодом и предотвращения дублирования кодов.
        """

        try:
            with transaction.atomic():
                RefBook.objects.create(
                    code='3',
                    name='Специальности медицинских работников',
                    description=''
                )
        except IntegrityError:
            self.fail("IntegrityError should not have been raised")

        with self.assertRaises(IntegrityError):
            RefBook.objects.create(
                code='1',
                name='Специальности медицинских работников',
                description=''
            )

    def test_duplicate_direction_version(self):
        """
        Тест для проверки создания версии справочника с уникальным
        номером версии и предотвращения дублирования номеров версий.
        """
        try:
            with transaction.atomic():
                RefBookVersion.objects.create(
                    ref_book_id=self.ref_book_1,
                    version='2.0',
                    start_date=date(2023, 8, 11)
                )
        except IntegrityError:
            self.fail('IntegrityError should not have been raised')

        with self.assertRaises(IntegrityError):
            RefBookVersion.objects.create(
                ref_book_id=self.ref_book_1,
                version='1.0',
                start_date=date(2023, 8, 11)
            )

    def test_duplicate_date_version(self):
        """
        Тест для проверки предотвращения создания версии с одинаковой датой начала действия.
        """

        with self.assertRaises(IntegrityError):
            RefBookVersion.objects.create(
                ref_book_id=self.ref_book_1,
                version='2.0',
                start_date=date(2023, 8, 10)
            )

    def test_duplicate_element_code_within_version(self):
        """
        Тест для проверки создания элементов справочника с уникальным кодом в пределах версии.
        """
        try:
            with transaction.atomic():
                RefBookElement.objects.create(
                    ref_book_version_id=self.ref_book_version_1,
                    code='4',
                    value='Травматолог'
                )
        except IntegrityError:
            self.fail('IntegrityError should not have been raised')

        with self.assertRaises(IntegrityError):
            RefBookElement.objects.create(
                ref_book_version_id=self.ref_book_version_2,
                code='2',
                value='Травматолог'
            )

    def test_api_get_ref_books(self):
        """
        Тест для проверки получения списка справочников через API.

        Получение списка справочников через API. Проверка соответствия ожидаемым данным.
        Получение списка справочников с фильтром по дате. Проверка соответствия ожидаемым данным.
        """

        response = self.client.get(reverse('ref_books:direction-list'))
        expected_content = [
            {'id': 1, 'code': '1', 'name': 'Специальности медицинских работников'},
            {'id': 2, 'code': '2', 'name': 'Должности медицинских работников'}
        ]
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        response = self.client.get(reverse('ref_books:direction-list'), {'date': '2023-08-10'})
        expected_content = [
            {'id': 1, 'code': '1', 'name': 'Специальности медицинских работников'},
        ]
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

    def test_api_ref_book_with_id_and_version(self):
        """
        Тест для проверки получения элементов справочника с указанным ID и версией через API.

        Получение списка элементов справочника с указанным ID через API без указания версии.
        Проверка соответствия ожидаемым данным.

        Получение списка элементов справочника с указанным ID через API с указанием версии 1.1.
        Проверка соответствия ожидаемым данным.

        Получение пустого списка элементов справочника с указанным ID через API с указанием версии 2.0.
        Проверка соответствия ожидаемым данным.
        """

        url = reverse('ref_books:element-list', kwargs={'id': self.ref_book_1.id})
        response = self.client.get(url)

        expected_content = [
            {'code': '1', 'value': 'Терапевт'},
            {'code': '2', 'value': 'Травматолог'},
            {'code': '3', 'value': 'Хирург'}
        ]
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        url = reverse('ref_books:element-list', kwargs={'id': self.ref_book_1.id})
        response = self.client.get(url, {'version': '1.1'})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        response = self.client.get(url, {'version': '2.0'})
        expected_content = []
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

    def test_api_validate_ref_books_elements_with_id_code_value_version(self):
        """
        Тест для проверки валидации элементов справочника через API.

        Попытка получения элементов справочника без указания параметров 'code' и 'value'.
        Ожидаем HTTP статус 400 и ожидаемый список ошибок.

        Получение элементов справочника по указанным параметрам 'code' и 'value'.
        Проверка соответствия ожидаемым данным.

        Получение пустого списка элементов справочника по указанным параметрам 'code', 'value' и версии 1.0.
        Проверка соответствия ожидаемым данным.

        Получение элементов справочника по указанным параметрам 'code', 'value' и версии 1.1.
        Проверка соответствия ожидаемым данным.
        """

        url = reverse('ref_books:check-element', kwargs={'id': self.ref_book_1.id})
        response = self.client.get(url)
        expected_content = ['Параметры "code" и "value" обязательны']
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        response = self.client.get(url, {'code': 1, 'value': 'Терапевт'})
        expected_content = [{'code': '1', 'value': 'Терапевт'}]
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        response = self.client.get(url, {'code': 1, 'value': 'Терапевт', 'version': '1.0'})
        expected_content = []
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)

        response = self.client.get(url, {'code': 1, 'value': 'Терапевт', 'version': '1.1'})
        expected_content = [{'code': '1', 'value': 'Терапевт'}]
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_json = json.dumps(response_data)
        expected_json = json.dumps(expected_content)
        self.assertJSONEqual(response_json, expected_json)
