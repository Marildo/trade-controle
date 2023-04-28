"""
 @author Marildo Cesar 26/04/2023
"""

from src.model import Ativo

data = Ativo.find_like_name('AMBEV')
print(data)