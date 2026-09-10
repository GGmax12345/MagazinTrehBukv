from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    """Одна карточка электроники в каталоге.

    Здесь хранятся данные, чтобы я мог выводить товары,
    искать их и менять в программе.
    """

    icon: str
    release_date: int
    name: str
    category: str
    price: int
    rating: float
    amount: int
    id: int | None = None

    def convert_date_to_str(self) -> str:
        """Преобразую год выпуска в строку, чтобы удобно выводить в консоль."""
        return str(self.release_date)
