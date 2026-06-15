"""
Главный модуль программы — пакетный анализатор данных

Реализует консольное меню и связывает все этапы конвейера обработки:
загрузка CSV, фильтрация, сортировка, поиск медианы,
скользящая сумма, гистограмма и откат состояний через стек
"""

import csv
import os
import random

from linked_list import LinkedList
from stack import Stack
from processing import (
    merge_sort,
    find_median,
    filter_outliers,
    build_prefix_sums,
    _mean,
    _std,
    plot_histogram,
)


def create_test_csv(filename="data.csv", n=100):
    """
    Создание тестового CSV-файла с одним столбцом чисел.
    Генерирует смесь нормально распределённых значений с несколькими
    выбросами для демонстрации фильтрации.
    """
    data = []
    for _ in range(n - 5):
        data.append(round(random.gauss(100, 15), 2))
    # Несколько выбросов
    for v in (250, 260, 10, 5, 300):
        data.append(round(random.gauss(v, 5), 2))
    random.shuffle(data)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["value"])
        for value in data:
            writer.writerow([value])

    print(f"Создан тестовый файл: {filename} ({n} записей)")


def load_csv(filename):
    """
    Загрузка данных из CSV-файла в массив и односвязный список
    Ожидается, что в файле есть заголовок 'value' в первой строке
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден.")

    data = []
    linked = LinkedList()

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        if header is None:
            raise ValueError("CSV-файл пуст.")

        for row in reader:
            if row:
                try:
                    value = float(row[0])
                    data.append(value)
                    linked.append(value)
                except ValueError:
                    print(f"Предупреждение: пропущена строка "
                          f"'{row[0]}' — не число.")

    if len(data) == 0:
        raise ValueError(
            "Не удалось загрузить ни одного числового значения."
        )

    return data, linked


def print_data(data, limit=20):
    """Вывод массива данных в консоль"""
    if len(data) == 0:
        print("[данные отсутствуют]")
        return

    if len(data) <= limit:
        print(f"Данные ({len(data)}): {data}")
    else:
        half = limit // 2
        print(f"Данные ({len(data)}): "
              f"{data[:half]} ... {data[-half:]}")


def main():
    """Главная функция — точка входа в программу"""
    data = None
    linked_list = None
    stack = Stack()

    # Автоматически создаём тестовый CSV, если файла нет
    if not os.path.exists("data.csv"):
        create_test_csv()

    while True:
        print(" 1. Загрузить CSV")
        print(" 2. Отфильтровать выбросы (3σ)")
        print(" 3. Отсортировать (merge sort)")
        print(" 4. Найти медиану")
        print(" 5. Префиксные суммы")
        print(" 6. Гистограмма")
        print(" 7. Откат (undo)")
        print(" 8. Показать данные")
        print(" 9. Показать статистику")
        print(" 0. Выход")

        choice = input("Выберите действие: ").strip()

        ## загрузка
        if choice == "1":
            filename = input(
                "Имя файла (по умолчанию data.csv): "
            ).strip()
            if filename == "":
                filename = "data.csv"
            try:
                data, linked_list = load_csv(filename)
                stack.push((list(data), "Загрузка из CSV"))
                print(f"Загружено {len(data)} записей.")
                print(f"Связный список: {linked_list}")
            except FileNotFoundError as e:
                print(f"Ошибка загрузки: {e}")
            except ValueError as e:
                print(f"Ошибка загрузки: {e}")

        elif data is None:
            print("Сначала загрузите данные (пункт 1).")
            continue

        ## фильтрация
        elif choice == "2":
            filtered, removed = filter_outliers(data)
            data = filtered
            stack.push((list(data), "Фильтрация (3σ)"))
            print(f"Удалено выбросов: {removed}. "
                  f"Осталось: {len(data)} элементов.")

        ## сортировка
        elif choice == "3":
            data = merge_sort(data)
            stack.push((list(data), "Сортировка (merge sort)"))
            print(f"Данные отсортированы. {len(data)} элементов.")

        ## медиана
        elif choice == "4":
            if len(data) == 0:
                print("Нет данных.")
                continue
            median_val = find_median(data)
            print(f"Медиана: {median_val}")

        ## префиксная сумма
        elif choice == "5":
            pref = build_prefix_sums(data)
            print(f"Префиксные суммы (первые 10): ", end="")
            if len(pref) <= 10:
                print(pref)
            else:
                print(pref[:10], "...")
            stack.push(
                (list(data), "Префиксные суммы")
            )

        ## гистограмма
        elif choice == "6":
            try:
                inp = input(
                    "Количество столбцов (по умолчанию 5): "
                ).strip()
                if inp == "":
                    bins = 5
                else:
                    bins = int(inp)
                if bins < 2:
                    bins = 2
                plot_histogram(data, bins)
            except ValueError:
                print("Введите целое число.")

        ## откат
        elif choice == "7":
            if stack.is_empty():
                print("Стек пуст. Некуда откатываться.")
            else:
                previous = stack.pop()
                if previous is not None:
                    data = previous[0]
                    label = previous[1]
                    print(f"Откат выполнен. "
                          f"Текущее состояние: {label}")
                    print(f"Элементов: {len(data)}")
                if stack.is_empty():
                    print("Достигнуто исходное состояние.")

        ## показать данные
        elif choice == "8":
            print_data(data)

        ## статистика
        elif choice == "9":
            if data is not None and len(data) > 0:
                mu = _mean(data)
                sigma = _std(data, mu)
                print(f"Количество элементов: {len(data)}")
                print(f"Минимум: {min(data):.2f}")
                print(f"Максимум: {max(data):.2f}")
                print(f"Среднее: {mu:.2f}")
                print(f"Стд. откл.: {sigma:.2f}")
            else:
                print("Нет данных.")

        ## выход
        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()