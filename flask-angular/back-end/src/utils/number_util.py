# @author Marildo Cesar 31/03/2024


def marred_five(value: float):
    """
    Arredonda um número para o múltiplo de 5 mais próximo.

    Args:
        value (float): Número a ser arredondado.
        multiple (float): Número a ser arredondado.

    Returns:
        float: Número arredondado para o múltiplo de 5 mais próximo.
    """

    diff = value % 5
    if diff >= 2.5:
        return value + (5 - diff)
    else:
        return value - diff


