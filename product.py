from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Product:
    """Одна карточка товара в каталоге.

    Здесь хранятся данные, чтобы я мог выводить товары,
    искать их и менять в программе.
    """

    icon: str
    release_date: date
    name: str
    category: str
    price: int
    rating: float
    amount: int
    id: int | None = None

    def convert_date_to_str(self) -> str:
        """Преобразую дату в формат ДД.ММ.ГГГГ, чтобы удобно выводить в консоль."""
        return self.release_date.strftime("%d.%m.%Y")
