"""
 @author Marildo Cesar 26/04/2023
"""

from src.model import Ativo, Feriados

f = Feriados.get(2024)
for i in f:
    print(i)

