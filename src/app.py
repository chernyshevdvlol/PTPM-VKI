import sqlite3
import math
from abc import ABC, abstractmethod



# a. Класс вычислений

class TriangleCalculator:
    def calculate(self, a_str, b_str, c_str):
        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
        except ValueError:
            return "", [(-2, -2), (-2, -2), (-2, -2)], "Введены нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Стороны должны быть положительными"

        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)], "Неравенство треугольника"

        if a == b == c:
            t_type = "равносторонний"
        elif a == b or a == c or b == c:
            t_type = "равнобедренный"
        else:
            t_type = "разносторонний"


        sides = sorted([a, b, c], reverse=True)
        a = sides[0]
        b = sides[1]
        c = sides[2]
        scale = 99 / a

        x1, y1 = 0, 0
        x2 = a * scale
        y2 = 0

        cos_angle = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        angle = math.acos(cos_angle)
        x3 = b * scale * math.cos(angle)
        y3 = b * scale * math.sin(angle)

        coords = [(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))]

        return t_type, coords, None


# b. Класс работы с базой данных

class Database:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS triangles (
                side_a REAL,
                side_b REAL,
                side_c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        ''')
        self.conn.commit()

    def save_result(self, a, b, c, t_type, error):
        self.cursor.execute('''
            INSERT OR REPLACE INTO triangles 
            (side_a, side_b, side_c, triangle_type, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (a, b, c, t_type, error))
        self.conn.commit()

    def get_result(self, a, b, c):
        self.cursor.execute('''
            SELECT triangle_type, error_message 
            FROM triangles 
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        ''', (a, b, c))
        return self.cursor.fetchone()

    def delete_result(self, a, b, c):
        self.cursor.execute('''
            DELETE FROM triangles 
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        ''', (a, b, c))
        self.conn.commit()

    def close(self):
        self.conn.close()

# c. Класс взаимодействия с пользователем

class UserInterface(ABC):
    @abstractmethod
    def get_input(self):
        pass


class ExternalService(ABC):
    @abstractmethod
    def send_data(self, data):
        pass


# d. Класс сторонней зависимости

class ConsoleUserInterface(UserInterface):
    def get_input(self):
        print("Введите три стороны треугольника:")
        a = input("Сторона A: ")
        b = input("Сторона B: ")
        c = input("Сторона C: ")
        return a, b, c


class EmailService(ExternalService):
    def send_data(self, data):
        print(f"[EmailService] Данные отправлены: {data}")
        return True


# e. Класс-контроллер

class Controller:

    def __init__(self, calculator, database, user_interface, external_service):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def process_request(self):

        # У пользователя запрашиваются входные данные
        a_str, b_str, c_str = self.user_interface.get_input()

        # Осуществляется проверка: если для данных нет записи в БД вычисляется результат и добавляется запись в БД; если для данных есть запись в БД  результат берется из БД.
        try:
            a, b, c = float(a_str), float(b_str), float(c_str)
            cached = self.database.get_result(a, b, c)
        except ValueError:
            cached = None

        if cached:
            # Данные есть в БД
            t_type, error = cached
            coords = []
            result = f"Тип: {t_type} (из кэша БД)"
        else:
            # Вычисляем результат
            t_type, coords, error = self.calculator.calculate(a_str, b_str, c_str)

            # Сохраняем в БД
            try:
                a, b, c = float(a_str), float(b_str), float(c_str)
                self.database.save_result(a, b, c, t_type, error)
            except ValueError:
                pass

            result = f"Тип: {t_type}, Координаты: {coords}"

        # Осуществляется отправка строки-результата сторонней зависимости
        self.external_service.send_data(result)

        # Метод возвращает результат выполнения операции.
        return result


if __name__ == "__main__":
    calculator = TriangleCalculator()
    database = Database("triangles.db")
    user_interface = ConsoleUserInterface()
    external_service = EmailService()

    controller = Controller(calculator, database, user_interface, external_service)

    result = controller.process_request()
    print(f"\nРезультат: {result}")

    database.close()