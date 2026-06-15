"""
Модуль конвейера: сортировка слиянием, фильтрация 3σ,
префиксные суммы, медиана, текстовая гистограмма
с рекурсивным разбиением диапазонов
"""

import math

def merge_sort(arr):
    """Рекурсивная сортировка слиянием"""
    if len(arr) <= 1:
        result = []
        for x in arr:
            result.append(x)
        return result

    mid = len(arr) // 2

    left_half = []
    for i in range(mid):
        left_half.append(arr[i])

    right_half = []
    for i in range(mid, len(arr)):
        right_half.append(arr[i])

    left = merge_sort(left_half)
    right = merge_sort(right_half)

    return _merge(left, right)

def _merge(left, right):
    """Слияние двух отсортированных списков в один"""
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1

    while i < len(left):
        result.append(left[i])
        i = i + 1

    while j < len(right):
        result.append(right[j])
        j = j + 1

    return result

def find_median(data):
    """Поиск медианы: сортировка слиянием и обращение по индексу"""
    sorted_data = merge_sort(data)
    mid_index = len(sorted_data) // 2
    return sorted_data[mid_index]

def _mean(arr):
    """Среднее арифметическое"""
    if len(arr) == 0:
        return 0.0
    total = 0.0
    for x in arr:
        total = total + x
    return total / len(arr)


def _std(arr, mu=None):
    """Стандартное отклонение (популяционное)"""
    if len(arr) < 2:
        return 0.0
    if mu is None:
        mu = _mean(arr)
    total = 0.0
    for x in arr:
        diff = x - mu
        total = total + diff * diff
    variance = total / len(arr)
    return math.sqrt(variance)

def filter_outliers(data):
    """Линейный поиск и удаление выбросов за пределами 3σ"""
    if len(data) < 2:
        copy = []
        for x in data:
            copy.append(x)
        return copy, 0

    mu = _mean(data)
    sigma = _std(data, mu)

    if sigma == 0:
        copy = []
        for x in data:
            copy.append(x)
        return copy, 0

    lower = mu - 3 * sigma
    upper = mu + 3 * sigma

    filtered = []
    removed = 0
    for x in data:
        if lower <= x <= upper:
            filtered.append(x)
        else:
            removed = removed + 1

    return filtered, removed

def build_prefix_sums(data):
    """Построение массива префиксных сумм"""
    if len(data) == 0:
        return []

    pref = []
    running_sum = 0.0
    for x in data:
        running_sum = running_sum + x
        pref.append(running_sum)

    return pref

def _split_range(data, num_parts):
    """Рекурсивное разбиение данных на части для гистограммы"""
    if num_parts <= 1:
        min_val = data[0]
        max_val = data[0]
        for x in data:
            if x < min_val:
                min_val = x
            if x > max_val:
                max_val = x
        return [min_val, max_val]

    sorted_data = merge_sort(data)
    mid = len(sorted_data) // 2
    median_val = sorted_data[mid]

    left = []
    right = []
    for x in data:
        if x <= median_val:
            left.append(x)
        else:
            right.append(x)

    if len(left) == 0:
        min_val = data[0]
        for x in data:
            if x < min_val:
                min_val = x
        left = [min_val]
    if len(right) == 0:
        max_val = data[0]
        for x in data:
            if x > max_val:
                max_val = x
        right = [max_val]

    left_parts = num_parts // 2
    right_parts = num_parts - left_parts

    left_edges = _split_range(left, left_parts)
    right_edges = _split_range(right, right_parts)

    result = []
    for edge in left_edges:
        result.append(edge)
    for i in range(1, len(right_edges)):
        result.append(right_edges[i])

    return result


def plot_histogram(data, num_bins=5):
    """Построение текстовой гистограммы в консоли"""
    if len(data) == 0:
        print("[Нет данных]")
        return

    if num_bins < 2:
        num_bins = 2
    if num_bins > len(data) // 2:
        num_bins = len(data) // 2
    if num_bins < 2:
        num_bins = 2

    edges = _split_range(data, num_bins)

    unique_edges = []
    for edge in edges:
        if edge not in unique_edges:
            unique_edges.append(edge)
    edges = merge_sort(unique_edges)

    n_bins = len(edges) - 1

    counts = []
    for i in range(n_bins):
        counts.append(0)

    for value in data:
        placed = False
        for i in range(n_bins):
            if i == n_bins - 1:
                if edges[i] <= value <= edges[i + 1]:
                    counts[i] = counts[i] + 1
                    placed = True
                    break
            else:
                if edges[i] <= value < edges[i + 1]:
                    counts[i] = counts[i] + 1
                    placed = True
                    break
        if not placed:
            for i in range(n_bins):
                if edges[i] <= value <= edges[i + 1]:
                    counts[i] = counts[i] + 1
                    break

    max_count = 0
    for c in counts:
        if c > max_count:
            max_count = c
    if max_count == 0:
        max_count = 1

    scale = 40 / max_count

    print()
    print("=" * 50)
    print("Гистограмма распределения")
    print("=" * 50)

    for i in range(n_bins):
        bar_len = int(counts[i] * scale)
        bar = ""
        for j in range(bar_len):
            bar = bar + "#"
        print(f"{edges[i]:>10.2f} - {edges[i+1]:>10.2f} | {bar} {counts[i]}")

    print("=" * 50)