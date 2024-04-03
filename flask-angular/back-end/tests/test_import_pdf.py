"""
 @author Marildo Cesar 23/04/2023
"""


def test_import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem

    file_name: str = "E:/developer/trade-controle/flask-angular/back-end/notas_pdf/nota-acoes-2024_03_28__2024_04_01_09_12.pdf"
    # file_name: str = "nota-futuro-2023_04_26.pdf"

    ready = ReadPDFCorretagem()
    ready.read(file_name)
    print(ready.notas())


test_import_corretagem()
