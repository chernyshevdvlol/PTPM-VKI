import unittest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from my_project import triangle


class TestTriangleProject(unittest.TestCase):

    # --- Базовые типы треугольников (1-3) ---
    def test_equilateral_triangle(self):
        # Равносторонний треугольник
        t_type, coords = triangle("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")

    def test_isosceles_triangle(self):
        # Равнобедренный треугольник
        t_type, coords = triangle("5", "5", "8")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene_triangle(self):
        # Разносторонний треугольник (классический 3-4-5)
        t_type, coords = triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    # --- Проверка невалидных числовых данных (4-7) ---
    def test_not_a_triangle_inequality(self):
        # Нарушение неравенства треугольника
        t_type, coords = triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side(self):
        # Отрицательная сторона
        t_type, coords = triangle("-5", "4", "3")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side(self):
        # Нулевая сторона
        t_type, coords = triangle("0", "5", "5")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_float_side(self):
        # Отрицательное дробное число
        t_type, coords = triangle("-3.14", "4", "5")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_float_side(self):
        # Нулевое дробное число
        t_type, coords = triangle("0.0", "5.5", "5.5")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    # --- Проверка нечислового ввода (8-11) ---
    def test_string_input_letters(self):
        # Ввод букв вместо чисел
        t_type, coords = triangle("abc", "2", "3")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_string_input_special_chars(self):
        # Ввод спецсимволов
        t_type, coords = triangle("!", "@", "#")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_mixed_valid_and_invalid_string(self):
        # Смешанный ввод: одно число, два нечисловых значения
        t_type, coords = triangle("5", "abc", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_empty_string_input(self):
        # Пустая строка вместо числа
        t_type, coords = triangle("", "5", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # --- Граничные и специфические случаи (12-20) ---
    def test_float_sides_valid(self):
        # Ввод корректных дробных чисел
        t_type, coords = triangle("2.5", "2.5", "2.5")
        self.assertEqual(t_type, "равносторонний")

    def test_large_sides(self):
        # Большие значения сторон
        t_type, coords = triangle("100", "100", "100")
        self.assertEqual(t_type, "равносторонний")

    def test_very_small_float_sides(self):
        # Очень маленькие дробные стороны
        t_type, coords = triangle("0.1", "0.1", "0.1")
        self.assertEqual(t_type, "равносторонний")

    def test_isosceles_with_large_base(self):
        # Равнобедренный с очень большим основанием (почти вырожденный)
        t_type, coords = triangle("10", "10", "19.9")
        self.assertEqual(t_type, "равнобедренный")

    def test_almost_degenerate_triangle(self):
        # Почти вырожденный разносторонний треугольник
        t_type, coords = triangle("10", "10.1", "19.99")
        self.assertEqual(t_type, "разносторонний")

    def test_spaces_in_input(self):
        # Ввод чисел с лишними пробелами (float() это корректно обрабатывает)
        t_type, coords = triangle(" 5 ", " 5 ", " 5 ")
        self.assertEqual(t_type, "равносторонний")

    def test_all_sides_different_large_floats(self):
        # Все стороны разные, большие дробные числа
        t_type, coords = triangle("100.5", "100.1", "100.9")
        self.assertEqual(t_type, "разносторонний")

    def test_right_triangle_coordinates_check(self):
        # Проверка, что координаты не равны ошибочным значениям для валидного треугольника
        t_type, coords = triangle("3", "4", "5")
        self.assertNotEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])
        self.assertNotEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])


if __name__ == '__main__':
    unittest.main()