"""
 @author Marildo Cesar 23/04/2023
"""


def test_import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem


    file_name: str = "nota-de-corretagem-2020.pdf"
    # file_name: str = "nota-futuro-2023_04_26.pdf"


    ready = ReadPDFCorretagem()
    ready.read(file_name)





test_import_corretagem()
