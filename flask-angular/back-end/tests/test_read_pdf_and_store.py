"""
 @author Marildo Cesar 25/04/2023
"""

from services.corretagem.read_pdf_file import ReadPDFCorretagem
from src.controller import OperacaoController, AtivoController

files = ("279757-BOV.pdf", "nota-de-corretagem-2021.pdf", "nota-de-corretagem-2020.pdf")

# AtivoController.find_by_or_save('LOCAMERICA/ON')


for i in files:
    ready = ReadPDFCorretagem()
    ready.read(i)
    operacoes = ready.operacoes()
    # print(operacoes)

    OperacaoController.save_operacoes(operacoes)
