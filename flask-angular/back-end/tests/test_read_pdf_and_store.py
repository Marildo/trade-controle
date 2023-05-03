"""
 @author Marildo Cesar 25/04/2023
"""

from services.corretagem.read_pdf_file import ReadPDFCorretagem
from src.controller import OperacaoController, AtivoController

# #,
files = ("nota-de-corretagem-2020.pdf", "nota-de-corretagem-2021.pdf", "nota-de-corretagem-2022.pdf",
         "nota-de-corretagem-2023.pdf",)

# AtivoController.find_by_or_save('LOCAMERICA/ON')


for i in files:
    ready = ReadPDFCorretagem()
    ready.read(i)
    notas = ready.notas()
    # print(operacoes)git

    OperacaoController.save_operacoes(notas)
