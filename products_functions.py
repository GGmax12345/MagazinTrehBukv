"""Функции для работы с каталогом товаров.

Здесь храним все операции: добавление, поиск, сортировка,
изменение, удаление и работа с файлами.
CRUD
"""

from product import Product
from datetime import date
from console_helper import *

SORT_BY_PRICE_ASC = 1
SORT_BY_PRICE_DESC = 2
SORT_BY_RATING_ASC = 3
SORT_BY_RATING_DESC = 4
SORT_BY_RELEASE_DATE_ASC = 5
SORT_BY_RELEASE_DATE_DESC = 6
SORT_BY_ID_ASC = 7
SORT_BY_ID_DESC = 8

SEARCH_BY_PART_NAME = 1
SEARCH_BY_CATEGORY = 2
SEARCH_BY_PRICE = 3


global_product_id = 0


def set_start_product_id(product_id: int):
    """Устанавливает значение счётчика ID после загрузки товаров из файла."""
    global global_product_id
    global_product_id = product_id


def get_next_product_id() -> int:
    """Увеличивает общий счётчик и возвращает новый уникальный ID."""
    global global_product_id

    global_product_id += 1

    return global_product_id


def input_product_data() -> Product:
    """Собирает данные о товаре из консоли и создаёт объект Product."""
    icon = input_str("Вставьте иконку товара: ", 1, 1)
    release_date = input_date(
        "Введите дату производства в формет ДД.ММ.ГГГГ: ",
        date(2026, 1, 1),
        date.today(),
    )
    name = input_str("Введите название товара (от 1 до 25 символов): ", 1, 25)
    category = input_str("Введите категорию товара (от 1 до 20 символов): ", 1, 20)
    price = input_int("Введите цену товара (от 1 до 10 000 000 руб.): ", 1, 10_000_000)
    rating = input_float("Введите рейтинг товара (от 1 до 5, можно дробный): ", 1, 5)
    amount = input_int(
        "Введите количество товара на складе (от 1 до 10 000 ед.): ", 1, 10_000
    )
    return Product(
        icon=icon,
        release_date=release_date,
        name=name,
        category=category,
        price=price,
        rating=rating,
        amount=amount,
    )


def get_product_by_id(products: list[Product], search_id: int) -> Product | None:
    """Ищет товар по ID; возвращает товар или None, если совпадения нет."""
    for product in products:
        if product.id == search_id:
            return product

    return None


def add_product_to_list(products: list[Product], product: Product):
    """Добавляет карточку товара в конец списка."""
    products.append(product)


def update_product_by_id(products: list[Product], product: Product) -> bool:
    """Заменяет данные товара с таким же ID и сообщает, получилось ли это."""
    find_product = get_product_by_id(products, product.id)

    if find_product == None:
        return False

    find_product.icon = product.icon
    find_product.release_date = product.release_date
    find_product.name = product.name
    find_product.category = product.category
    find_product.price = product.price
    find_product.rating = product.rating
    find_product.amount = product.amount

    return True


def delete_product_by_id(products: list[Product], search_id: int) -> bool:
    """Удаляет товар с нужным ID и возвращает результат операции."""
    find_product = get_product_by_id(products, search_id)

    if find_product == None:
        return False

    products.remove(find_product)

    return True


def print_table_products_header():
    """Печатает названия столбцов таблицы товаров."""
    print(
        f"{'ИД':<5}"
        f"{'Иконка':<15}"
        f"{'Дата выпуска':<20}"
        f"{'Название':<35}"
        f"{'Категория':<20}"
        f"{'Цена(руб.)':<12}"
        f"{'Рейтинг':<10}"
        f"{'Количество':<12}"
    )


def print_single_product(product: Product):
    """Печатает одну карточку товара как строку таблицы."""
    print(
        f"{product.id:<5}"
        f"{product.icon:<15}"
        f"{product.convert_date_to_str():<20}"
        f"{product.name:<35}"
        f"{product.category:<20}"
        f"{product.price:<12}"
        f"{product.rating:<10}"
        f"{product.amount:<12}"
    )


def print_all_products(products: list[Product]):
    """Печатает заголовок и все товары либо сообщение о пустом списке."""
    print_table_products_header()

    if len(products) > 0:
        for product in products:
            print_single_product(product)
    else:
        print("Список товаров пуст")


def sort_products_by_type_sort(products: list[Product], type_sort: int):
    """Сортирует исходный список товаров выбранным способом методом пузырька.

    Функция меняет порядок элементов прямо в переданном списке и ничего не
    возвращает. На каждом проходе соседние товары сравниваются и при необходимости
    меняются местами. После полного прохода один элемент уже оказывается на своём
    месте, поэтому ``offset`` сокращает проверяемую часть списка.
    """
    if type_sort == SORT_BY_PRICE_ASC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].price < products[i].price:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_PRICE_DESC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].price > products[i].price:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_RATING_ASC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].rating < products[i].rating:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_RATING_DESC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].rating > products[i].rating:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_RELEASE_DATE_ASC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].release_date < products[i].release_date:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_RELEASE_DATE_DESC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].release_date > products[i].release_date:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_ID_ASC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].id < products[i].id:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1
    elif type_sort == SORT_BY_ID_DESC:
        offset = 0
        temp = None
        is_sort = False

        while is_sort == False:
            is_sort = True

            for i in range(0, len(products) - 1 - offset):
                if products[i + 1].id > products[i].id:
                    temp = products[i]
                    products[i] = products[i + 1]
                    products[i + 1] = temp

                    is_sort = False

            offset += 1


def find_products_by_type_search(
    products: list[Product], type_search: int, parameter: str
) -> list[Product]:
    """Возвращает товары, найденные выбранным способом поиска.

    Доступны поиск по части названия, по категории и по диапазону цены.
    Исходный список не изменяется.
    """
    if type_search == SEARCH_BY_PART_NAME:
        finded_products = []
        parameter = parameter.strip()

        for product in products:
            if parameter.lower() in product.name.lower():
                finded_products.append(product)

        return finded_products

    elif type_search == SEARCH_BY_CATEGORY:
        finded_products = []
        parameter = parameter.strip()

        for product in products:
            if parameter.lower() in product.category.lower():
                finded_products.append(product)

        return finded_products

    elif type_search == SEARCH_BY_PRICE:
        finded_products = []
        parameter = parameter.strip()

        min_price = int(parameter.split("|")[0])
        max_price = int(parameter.split("|")[1])

        for product in products:
            if product.price >= min_price and product.price <= max_price:
                finded_products.append(product)

        return finded_products



def buy_product(products: list[Product], search_id: int, request_amount: int) -> bool:
    """Уменьшает остаток товара и возвращает True при успешной покупке.

    Покупка не состоится, если товар не найден или на складе недостаточно
    единиц; в этих случаях функция возвращает False.
    """
    find_product = get_product_by_id(products, search_id)

    if find_product == None:
        return False

    if find_product.amount < request_amount:
        return False

    find_product.amount -= request_amount

    return True


def load_products_from_txt_file(filename: str) -> list[Product]:
    """Загружает список товаров из служебного текстового файла.

    Формат файла построчный: сначала количество товаров и последнее выданное ID,
    затем для каждого товара идут восемь строк с его полями. При любой ошибке
    открытия, преобразования или структуры функция возвращает None.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file_in:
            products = []
            count_products = int(file_in.readline())

            set_start_product_id(int(file_in.readline()))

            for _ in range(count_products):
                products.append(
                    Product(
                        id=int(file_in.readline()),
                        icon=file_in.readline().strip(),
                        release_date=datetime.strptime(
                            file_in.readline().strip(), "%d.%m.%Y"
                        ).date(),
                        name=file_in.readline().strip(),
                        category=file_in.readline().strip(),
                        price=int(file_in.readline()),
                        rating=float(file_in.readline()),
                        amount=int(file_in.readline()),
                    )
                )

            return products
    except:
        return None


def save_products_to_txt_file(products: list[Product], filename: str) -> bool:
    """Сохраняет данные в служебном формате для последующей загрузки.

    В отличие от печатной таблицы, здесь каждое значение занимает отдельную
    строку. Непустой каталог можно прочитать функцией
    load_products_from_txt_file(); файл с пустым каталогом текущий загрузчик не поддерживает.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file_out:
            file_out.write(f"{len(products)}\n")

            if len(products) > 0:
                file_out.write(f"{global_product_id}\n")
                for product in products:
                    file_out.write(
                        f"{product.id}\n"
                        f"{product.icon}\n"
                        f"{product.convert_date_to_str()}\n"
                        f"{product.name}\n"
                        f"{product.category}\n"
                        f"{product.price}\n"
                        f"{product.rating}\n"
                        f"{product.amount}\n"
                    )
            else:
                file_out.write("Список товаров пуст")

        return True
    except:
        return False


def save_products_to_txt_file_for_print(products: list[Product], filename: str) -> bool:
    """Сохраняет список товаров в виде таблицы, удобной для чтения и печати.

    Это отдельный, человекочитаемый формат. Его нельзя передавать функции
    load_products_from_txt_file(), потому что расположение данных в нём другое.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file_out:
            file_out.write("Список товаров магазина NeDikayaMalina\n\n")

            file_out.write(
                f"{'ИД':<5}"
                f"{'Иконка':<15}"
                f"{'Дата выпуска':<20}"
                f"{'Название':<35}"
                f"{'Категория':<20}"
                f"{'Цена(руб.)':<12}"
                f"{'Рейтинг':<10}"
                f"{'Количество':<12}"
                "\n"
            )

            if len(products) > 0:
                for product in products:
                    file_out.write(
                        f"{product.id:<5}"
                        f"{product.icon:<15}"
                        f"{product.convert_date_to_str():<20}"
                        f"{product.name:<35}"
                        f"{product.category:<20}"
                        f"{product.price:<12}"
                        f"{product.rating:<10}"
                        f"{product.amount:<12}"
                        "\n"
                    )
            else:
                file_out.write("Список товаров пуст")

        return True
    except:
        return False
