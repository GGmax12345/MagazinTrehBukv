from datetime import date, datetime


def input_int(message: str, min_val: int, max_val: int) -> int:
    """Просит ввести целое число и повторяет вопрос, пока число не подойдёт.

    Это удобно, потому что пользователь может случайно написать букву,
    отрицательное число или число за границами допустимого диапазона.
    """
    is_correct_input = False
    input_int = 0

    while is_correct_input == False:
        try:
            input_int = int(input(message))

            if input_int < min_val or input_int > max_val:
                print(
                    f"Ошибка ввода. Введённое число должно быть от {min_val} до {max_val}"
                )
            else:
                is_correct_input = True
        except:
            print(f"Ошибка ввода. Вы ввели не целое число")

    return input_int


def input_float(message: str, min_val: float, max_val: float) -> float:
    """Просит ввести число с дробной частью и снова спрашивает при ошибке.

    Здесь нужны дробные числа, например рейтинг товара. Вводить надо
    через точку: 4.5, а не через запятую.
    """
    is_correct_input = False
    input_int = 0

    while is_correct_input == False:
        try:
            input_int = float(input(message))

            if input_int < min_val or input_int > max_val:
                print(
                    f"Ошибка ввода. Введённое число должно быть от {min_val} до {max_val}"
                )
            else:
                is_correct_input = True
        except:
            print(f"Ошибка ввода. Вы ввели не целое число")

    return input_int


def input_str(message: str, min_len: int, max_len: int) -> str:
    """Просит ввести текст заданной длины и не даёт уйти дальше при ошибке.

    Я проверяю только количество символов. Если строка слишком короткая или
    слишком длинная, программа снова просит ввести её заново.
    """
    is_correct_input = False
    input_str = ""

    while is_correct_input == False:
        input_str = input(message)

        if len(input_str) < min_len or len(input_str) > max_len:
            print(
                f"Ошибка ввода. Введённая строка по длине должна быть от {min_len} до {max_len} символов"
            )
        else:
            is_correct_input = True

    return input_str


def input_date(message: str, min_date: date, max_date: date) -> date:
    """Просит ввести дату в формате ДД.ММ.ГГГГ и проверяет диапазон.

    После этого дата хранится как объект date, и я могу сравнивать её с
    другими датами, не разбирать строку вручную.
    """
    is_correct_input = False
    input_date = date.today()

    while is_correct_input == False:
        try:
            input_date = datetime.strptime(input(message), "%d.%m.%Y").date()

            if input_date < min_date or input_date > max_date:
                print(
                    f"Ошибка ввода. Введённая дата должна быть от {min_date.strftime('%d.%m.%Y')} до {max_date.strftime('%d.%m.%Y')}"
                )
            else:
                is_correct_input = True
        except:
            print(f"Ошибка ввода. Вы ввели дату не в формате ДД.ММ.ГГГГ")

    return input_date


def print_devider(devider: str, len_diveder: int):
    """Печатает строку-разделитель указанное число раз."""
    print(devider * len_diveder)


def wait_enter():
    """Отделяет вывод и ждёт нажатия Enter."""
    print("\n\n")
    print_devider("=", 125)
    print("\n\nДля продолжения работы нажмите <Enter>\n\n")
    input()
