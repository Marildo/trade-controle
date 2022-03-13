class StrUtil:

    @staticmethod
    def str_to_float(value: str) -> float:
        value = value.replace(',','.')
        return float(value)