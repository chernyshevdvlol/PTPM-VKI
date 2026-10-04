import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from delivery_service import calculate_delivery_cost


class TestDeliveryService(unittest.TestCase):

    def test_normal_delivery(self):
        # Обычная доставка, нормальный вес
        cost, date = calculate_delivery_cost(10.0, 1000, "обычный", False)
        self.assertGreater(cost, 0)
        self.assertRegex(date, r"\d{4}-\d{2}-\d{2}")

    def test_fragile_package(self):
        # Хрупкая посылка (должна быть дороже)
        cost_normal, _ = calculate_delivery_cost(10.0, 1000, "обычный", False)
        cost_fragile, _ = calculate_delivery_cost(10.0, 1000, "хрупкий", False)
        self.assertGreater(cost_fragile, cost_normal)

    def test_dangerous_package(self):
        # Опасная посылка (должна быть самой дорогой)
        cost, _ = calculate_delivery_cost(10.0, 1000, "опасный", False)
        self.assertGreater(cost, 5000)

    def test_heavy_package_over_20kg(self):
        # Тяжелая посылка > 20 кг (коэффициент 1.5)
        cost, _ = calculate_delivery_cost(25.0, 1000, "обычный", False)
        self.assertGreater(cost, 6000)

    def test_weight_exactly_5kg(self):
        # Вес ровно 5.0 кг (БАГ: в коде стоит > 5.0, а должно быть >= 5.0)
        cost, _ = calculate_delivery_cost(5.0, 1000, "обычный", False)
        cost_5_1, _ = calculate_delivery_cost(5.1, 1000, "обычный", False)
        # Этот тест упадет, потому что код не применяет наценку к 5.0
        self.assertEqual(cost, cost_5_1, "Вес 5.0 кг должен обрабатываться так же, как 5.1 кг")

    def test_weight_under_minimum(self):
        # Вес ниже минимального (0.1 кг)
        cost, date = calculate_delivery_cost(0.05, 1000, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_over_maximum(self):
        # Расстояние выше максимального (5000 км)
        cost, date = calculate_delivery_cost(10.0, 6000, "обычный", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        # Неверный тип посылки
        cost, date = calculate_delivery_cost(10.0, 1000, "мокрый", False)
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_express_delivery_cost_bug(self):
        # Экспресс-доставка (БАГ: в коде стоимость умножается на 0.5, то есть дешевеет!)
        cost_normal, _ = calculate_delivery_cost(10.0, 1000, "обычный", False)
        cost_express, _ = calculate_delivery_cost(10.0, 1000, "обычный", True)
        # Этот тест упадет, так как cost_express окажется меньше cost_normal
        self.assertGreater(cost_express, cost_normal, "Экспресс-доставка должна быть дороже обычной")

    def test_express_delivery_time_bug(self):
        # Экспресс-доставка на короткое расстояние (БАГ: 400 // 500 = 0, 0 // 2 = 0 дней)
        cost, date = calculate_delivery_cost(10.0, 400, "обычный", True)
        # Этот тест упадет, потому что дата доставки не может быть раньше или равна дате отправки (2026-09-03)
        self.assertGreater(date, "2026-09-03", "Минимальный срок доставки даже экспрессом должен быть > 0 дней")


if __name__ == '__main__':
    unittest.main()