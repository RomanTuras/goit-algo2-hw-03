import csv
import timeit
from BTrees.OOBTree import OOBTree


# Функція для завантаження даних з CSV
def load_data(filename):
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            data.append(item)
    return data


# Функція для додавання товару в OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


# Функція для додавання товару в dict
def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


# Функція для діапазонного запиту в OOBTree
def range_query_tree(tree, min_price, max_price):
    return [
        (item_id, data)
        for item_id, data in tree.items()
        if min_price <= data["Price"] <= max_price
    ]


# Функція для діапазонного запиту в dict
def range_query_dict(dictionary, min_price, max_price):
    return [
        (item_id, data)
        for item_id, data in dictionary.items()
        if min_price <= data["Price"] <= max_price
    ]


# Основна функція
def main():
    # Завантаження даних
    data = load_data("generated_items_data.csv")

    # Ініціалізація структур
    tree = OOBTree()
    dictionary = {}

    # Додавання товарів у структури
    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначення діапазону цін
    min_price = 50.0
    max_price = 150.0

    # Вимірювання часу для OOBTree
    tree_time = timeit.timeit(
        stmt=lambda: range_query_tree(tree, min_price, max_price), number=100
    )

    # Вимірювання часу для dict
    dict_time = timeit.timeit(
        stmt=lambda: range_query_dict(dictionary, min_price, max_price), number=100
    )

    # Виведення результатів
    print(f"Загальний час range_query для OOBTree: {tree_time:.6f} сек")
    print(f"Загальний час range_query для Dict: {dict_time:.6f} сек")


if __name__ == "__main__":
    main()
