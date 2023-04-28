"""
 @author Marildo Cesar 23/04/2023
"""


def test_import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem
    from src.model import Operacoes

    file_name: str = "nota-de-corretagem-2021.pdf"
    # file_name = 'C:/Users/Cesar/Downloads/nota-futuro-2022_06_03.pdf'
    # file_name ='C:/Users/Cesar/Downloads/nota-futuro-2022_05_19.pdf'

    ready = ReadPDFCorretagem()
    ready.read(file_name)





test_import_corretagem()
