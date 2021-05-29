"""Модуль содержащий генератор хэш значений для ссылки."""

import random
import string


def hash_generator():
    """Сгенерировать случайный хэш из 8-12 символов для ссылки."""
    length = random.randint(8, 12)
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, length))
