"""Enum возможных типов устройств."""
import enum


class LinkTypes(enum.Enum):
    """Перечисление возможных типов утройств."""

    PUBLIC = 0
    ONLY_AUTH = 1
    PERSONAL = 2

    @classmethod
    def all_link_types(cls):
        return [
            cls.PUBLIC.value,
            cls.ONLY_AUTH.value,
            cls.PERSONAL.value,
        ]