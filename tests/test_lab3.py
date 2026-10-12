import unittest
from unittest.mock import patch, MagicMock
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from app import TriangleCalculator, Database, Controller, ConsoleUserInterface


class TestLab3(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")
        self.calculator = TriangleCalculator()

    def tearDown(self):
        self.db.close()

    # Интеграционные тесты
    # Данные которых нет в БД
    @patch.object(ConsoleUserInterface, 'get_input', return_value=("3", "4", "5"))
    def test_process_request_new_data(self, mock_input):

        mock_service = MagicMock()
        controller = Controller(self.calculator, self.db, ConsoleUserInterface(), mock_service)

        result = controller.process_request()

        mock_service.send_data.assert_called_once()
        self.assertIn("разносторонний", result)

    # Данные уже есть в БД
    @patch.object(ConsoleUserInterface, 'get_input', return_value=("5", "5", "5"))
    def test_process_request_cached_data(self, mock_input):

        self.db.save_result(5.0, 5.0, 5.0, "равносторонний", None)

        mock_service = MagicMock()
        controller = Controller(self.calculator, self.db, ConsoleUserInterface(), mock_service)

        result = controller.process_request()


        mock_service.send_data.assert_called_once()
        self.assertIn("из кэша БД", result)
        self.assertIn("равносторонний", result)


    # Буквы вместо чисел
    @patch.object(ConsoleUserInterface, 'get_input', return_value=("abc", "2", "3"))
    def test_process_request_invalid_input(self, mock_input):
        mock_service = MagicMock()
        controller = Controller(self.calculator, self.db, ConsoleUserInterface(), mock_service)

        result = controller.process_request()

        mock_service.send_data.assert_called_once()
        self.assertIn("Тип:", result)

    # Юнит тесты
    # Проверка методов БД (сохранить, получить, удалить)
    def test_database_save_get_delete(self):
        # Сохранить
        self.db.save_result(10.0, 10.0, 10.0, "равносторонний", None)

        # Получить
        result = self.db.get_result(10.0, 10.0, 10.0)

        # Проверка
        self.assertEqual(result[0], "равносторонний")

        # Удалить
        self.db.delete_result(10.0, 10.0, 10.0)

        # Проверка
        self.assertIsNone(self.db.get_result(10.0, 10.0, 10.0))

    # Калькулятор возвращает ошибку при не числовых значениях
    def test_calculator_returns_error_for_invalid(self):
        t_type, coords, error = self.calculator.calculate("aabbcc", "5", "5")

        self.assertIsNotNone(error)
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


if __name__ == '__main__':
    unittest.main()