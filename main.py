"""Каталог товаров для магазина электроники.

Я делал проект шаг за шагом по методичке: сначала сделал данные товара,
потом функции для поиска и сортировки, а в конце собрал меню.
"""

from product import Product
from datetime import date
import os
import sys
from pathlib import Path

from console_helper import *
from products_functions import *

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_env_file() -> None:
    """Читает переменные из .env, если они не заданы в окружении."""
    env_path = Path(__file__).resolve().with_name(".env")

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env_file()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

products: list[Product] = load_products_from_txt_file("prod.dat") or []


def print_products():
    """Показывает каталог в начале работы и перед возвратом в меню."""
    print("Список товаров магазина электроники")
    print_all_products(products)
    print_devider("=", 125)


def print_main_menu():
    """Показывает пункты главного меню."""
    print("Главное меню:")
    print("1. Меню Покупателя")
    print("2. Меню Администратора")
    print("0. Выход")


def work_with_sort_products_sub_menu():
    """Предлагает способ сортировки и меняет порядок товаров в каталоге."""
    global products

    print("Меню Сортировки:")
    print("1. По возрастанию цены")
    print("2. По убыванию цены")
    print("3. По возрастанию рейтинга")
    print("4. По убыванию рейтинга")
    print("5. По возрастанию даты выпуска")
    print("6. По убыванию даты выпуска")
    print("7. По возрастанию ID")
    print("8. По убыванию ID")

    choosen_action = input_int("Выберите пункт меню: ", 1, 8)

    if choosen_action == 1:
        sort_products_by_type_sort(products, SORT_BY_PRICE_ASC)
    elif choosen_action == 2:
        sort_products_by_type_sort(products, SORT_BY_PRICE_DESC)
    elif choosen_action == 3:
        sort_products_by_type_sort(products, SORT_BY_RATING_ASC)
    elif choosen_action == 4:
        sort_products_by_type_sort(products, SORT_BY_RATING_DESC)
    elif choosen_action == 5:
        sort_products_by_type_sort(products, SORT_BY_RELEASE_DATE_ASC)
    elif choosen_action == 6:
        sort_products_by_type_sort(products, SORT_BY_RELEASE_DATE_DESC)
    elif choosen_action == 7:
        sort_products_by_type_sort(products, SORT_BY_ID_ASC)
    elif choosen_action == 8:
        sort_products_by_type_sort(products, SORT_BY_ID_DESC)

    print("Отсортированный список товаров")
    print_all_products(products)
    print_devider("=", 125)


def work_with_find_products_sub_menu():
    """Ищет товары по выбранному критерию и печатает результат."""
    global products

    print("Меню Поиска:")
    print("1. По имени")
    print("2. По категории")
    print("3. По диапазону цены")

    choosen_action = input_int("Выберите пункт меню: ", 1, 3)

    finded_products = []

    if choosen_action == 1:
        name = input_str(
            "Введите название товара для поиска (от 1 до 25 символов): ", 1, 25
        )

        finded_products = find_products_by_type_search(
            products, SEARCH_BY_PART_NAME, name
        )

    elif choosen_action == 2:
        category = input_str(
            "Введите категорию товара для поиска (от 1 до 20 символов): ", 1, 20
        )

        finded_products = find_products_by_type_search(
            products, SEARCH_BY_CATEGORY, category
        )
    elif choosen_action == 3:
        min_price = input_int(
            "Введите минимальную цену товара для поиска (от 1 до 10 000 000 руб.): ",
            1,
            10_000_000,
        )

        max_price = input_int(
            "Введите максимальную цену товара для поиска (от 1 до 10 000 000 руб.): ",
            1,
            10_000_000,
        )

        prices_as_str = f"{min_price}|{max_price}"

        finded_products = find_products_by_type_search(
            products, SEARCH_BY_PRICE, prices_as_str
        )

    print("Найденные товары")
    if len(finded_products) > 0:
        print_table_products_header()
        print_all_products(finded_products)
    else:
        print("Товары не найдены")


def work_with_buyer_menu():
    """Показывает меню покупателя, пока пользователь не решит выйти из него."""
    global products

    is_run = True
    while is_run == True:
        print("Меню Покупателя:")
        print("1. Найти товар по ID")
        print("2. Сортировать товары")
        print("3. Найти товары")
        print("4. Купить товар")
        print("5. Сохранить товары в текстовый файл для печати")
        print("0. В Главное меню")

        choosen_action = input_int("Выберите пункт меню: ", 0, 7)

        if choosen_action == 1:
            search_id = input_int("Введите ID товара для поиска: ", 1, 2_000_000_000)
            found_product = get_product_by_id(products, search_id)

            if found_product == None:
                    print(f"Электронное устройство с ID {search_id} не найдено")
            else:
                print_table_products_header()
                print_single_product(found_product)
        elif choosen_action == 2:
            work_with_sort_products_sub_menu()
        elif choosen_action == 3:
            work_with_find_products_sub_menu()
        elif choosen_action == 4:
            search_id = input_int("Введите ID товара для покупки: ", 1, 2_000_000_000)
            request_amount = input_int(
                "Введите количество товара для покупки: ", 1, 10_000
            )
            is_bought = buy_product(products, search_id, request_amount)

            if is_bought == False:
                print(
                    "Ошибка покупки товара проверьте что Вы ввели верный ID товара и товара достаточно на складе"
                )
            else:
                print("Товар успешно куплен")
        elif choosen_action == 5:
            filename = input_str("Введите имя файла для сохранения: ", 4, 100)

            is_saved = save_products_to_txt_file_for_print(products, filename)

            if is_saved == False:
                print("Ошибка сохранения файла")
            else:
                print("Файл успешно сохранён")
        elif choosen_action == 0:
            is_run = False

        wait_enter()


def auth_is_administrator():
    """Проверяет пароль и возвращает True, если он правильный."""
    password = input_str(
        "Введите пароль Администратора для входа в Меню Администратора: ", 4, 16
    )
    return password == ADMIN_PASSWORD


def work_with_administrator_menu():
    """Обрабатывает команды меню администратора."""
    global products

    is_run = True
    while is_run == True:
        print("Меню Администратора:")
        print("1. Найти товар по ID")
        print("2. Добавить новый товар")
        print("3. Изменить товар по ID")
        print("4. Удалить товар по ID")
        print("5. Загрузить товары из текстового файла")
        print("6. Сохранить товары в текстовый файл")
        print("7. Сохранить товары в текстовый файл для печати")
        print("0. В Главное меню")

        choosen_action = input_int("Выберите пункт меню: ", 0, 7)

        if choosen_action == 1:
            search_id = input_int("Введите ID товара для поиска: ", 1, 2_000_000_000)
            found_product = get_product_by_id(products, search_id)

            if found_product == None:
                    print(f"Электронное устройство с ID {search_id} не найдено")
            else:
                print_table_products_header()
                print_single_product(found_product)
        elif choosen_action == 2:
            print("Введите данные нового продукта")

            new_product = input_product_data()

            new_product.id = get_next_product_id()

            add_product_to_list(products, new_product)

            print("Электронное устройство успешно добавлено")
        elif choosen_action == 3:
            update_id = input_int(
                "Введите ID товара для обновления: ", 1, 2_000_000_000
            )
            found_product = get_product_by_id(products, update_id)

            if found_product == None:
                print(f"Электронное устройство с ID {update_id} не найдено")
            else:
                print("Введите новые данные для электронного устройства")

                update_product = input_product_data()

                update_product.id = update_id

                update_product_by_id(products, update_product)

                print("Электронное устройство успешно обновлено")

        elif choosen_action == 4:
            delete_id = input_int("Введите ID товара для удаления: ", 1, 2_000_000_000)

            is_deleted = delete_product_by_id(products, delete_id)

            if is_deleted == False:
                    print(f"Электронное устройство с ID {delete_id} не найдено")
            else:
                    print("Электронное устройство успешно удалено")
        elif choosen_action == 5:
            filename = input_str("Введите имя файла для загрузки: ", 4, 100)

            products = load_products_from_txt_file(filename)

            if products == None:
                print(
                    "Ошибка загрузки файла. Используйте служебный файл данных, созданный командой 'Сохранить товары в текстовый файл'. Файл для печати загружать нельзя."
                )
            else:
                print("Файл успешно загружен")

        elif choosen_action == 6:
            filename = input_str("Введите имя файла для сохранения: ", 4, 100)

            is_saved = save_products_to_txt_file(products, filename)

            if is_saved == False:
                print("Ошибка сохранения файла")
            else:
                print("Файл успешно сохранён")
        elif choosen_action == 7:
            filename = input_str("Введите имя файла для сохранения: ", 4, 100)

            is_saved = save_products_to_txt_file_for_print(products, filename)

            if is_saved == False:
                print("Ошибка сохранения файла")
            else:
                print("Файл успешно сохранён")

        elif choosen_action == 0:
            is_run = False

        wait_enter()


def main():
    """Запускает основное меню и обработку действий пользователя."""
    is_run = True

    while is_run == True:
        print_products()

        print_main_menu()
        choosen_action = input_int("Выберите пункт меню: ", 0, 2)

        if choosen_action == 1:
            work_with_buyer_menu()
        elif choosen_action == 2:
            if auth_is_administrator() == True:
                print("Пароль успешно введён")
                work_with_administrator_menu()
            else:
                print("Ошибка ввода пароля администратора")
        elif choosen_action == 0:
            is_run = False


if __name__ == "__main__":
    main()
