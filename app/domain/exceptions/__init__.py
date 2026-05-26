class DomainError(Exception):
    """Базовый класс доменных ошибок."""


class NotFoundError(DomainError):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(f"{entity} с ID {entity_id} не найден")


class OutOfStockError(DomainError):
    def __init__(self, product_name: str, available: int, requested: int):
        super().__init__(
            f"Недостаточно товара '{product_name}': в наличии {available}, запрошено {requested}"
        )


class InvalidStatusError(DomainError):
    ALLOWED = {"pending", "confirmed", "shipped", "delivered", "cancelled"}

    def __init__(self, status: str):
        super().__init__(f"Недопустимый статус '{status}'. Допустимые: {', '.join(self.ALLOWED)}")
