"""
 @author Marildo Cesar 22/04/2023
"""

from re import sub


def str_to_float(value: str) -> float:
    value = value.replace('.', '').replace(',', '.')
    if not value.strip():
        return 0.0
    return float(value)


def onnly_numbers(value: str) -> str:
    return sub(r'\D', '', value)


def capitalize_plus(value: str) -> str:
    return value.replace('_', ' ').capitalize()
