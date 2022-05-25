import re


class StrUtil:

    @staticmethod
    def str_to_float(value: str) -> float:
        value = value.replace('.', '').replace(',', '.')
        return float(value)

    @staticmethod
    def onnly_numbers(value: str) -> str:
        return re.sub(r'\D', '', value)
