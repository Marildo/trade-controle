"""
 @author Marildo Cesar 23/04/2023
"""


def test_import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem


    file_name: str = "E:/developer/trade-controle/flask-angular/back-end/notas_pdf/2024-02-14_stock__2024_02_15_16_37.pdf"
    # file_name: str = "nota-futuro-2023_04_26.pdf"


    ready = ReadPDFCorretagem()
    ready.read(file_name)





test_import_corretagem()
