import math
import logging
import sys
# Шаблон строки лога (аналог template в Serilog)
# Содержит: время, уровень (до 7 символов для выравнивания), имя логгера и сообщение
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Базовая настройка корневого логгера
logging.basicConfig(
    level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),          # Настройка логирования в консоль
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8") # Настройка логирования в файл
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

def main():

    print("Вид треугольника и координаты вершин\n")

    a_str = input("Сторона A: ")
    b_str = input("Сторона B: ")
    c_str = input("Сторона C: ")

    logging.debug(f"Входные данные: A='{a_str}', B='{b_str}', C='{c_str}'")

    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)


    except ValueError:
        logging.error(f"Введены нечисловые данные: A='{a_str}', B='{b_str}', C='{c_str}'")
        print("\nВведены нечисловые данные")

        print("Тип треугольника: ")
        print("Координаты вершин: [(-2, -2), (-2, -2), (-2, -2)]")
        exit()

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning(f"Отрицательные или нулевые значения: a={a}, b={b}, c={c}")
        print("\nСтороны должны быть положительными")
        print("Тип треугольника: не треугольник")
        print("Координаты вершин: [(-1, -1), (-1, -1), (-1, -1)]")
        exit()

    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning(f"Неравенство треугольника у сторон: {a}, {b}, {c}")
        print("\nТип треугольника: не треугольник")
        print("Координаты вершин: [(-1, -1), (-1, -1), (-1, -1)]")
        exit()

    if a == b == c:
        t_type = "равносторонний"
    elif a == b or a == c or b == c:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"

#------
    sides = sorted([a, b, c], reverse=True)
    a = sides[0]
    b = sides[1]
    c = sides[2]

    scale = 99 / a

    x1, y1 = 0, 0
    x2 = a * scale
    y2 = 0
#теорема косинусов
    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    angle = math.acos(cos_angle)

    x3 = b * scale * math.cos(angle)
    y3 = b * scale * math.sin(angle)

    coords = [(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))]
    logging.info(f"Успех. Тип: '{t_type}', Координаты: {coords}")

    print(f"\nРезультат:")
    print(f"Тип треугольника: {t_type}")
    print(f"Координаты вершин: {coords}")
if __name__ == "__main__":
    main()