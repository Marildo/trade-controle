"""
 @author Marildo Cesar 23/04/2023
"""


def test_import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem


    file_name: str = "D:/developer/trade-controle/flask-angular/back-end/notas_pdf/2023-07-05_future__2023_07_08_10_25.pdf"
    # file_name: str = "nota-futuro-2023_04_26.pdf"


    ready = ReadPDFCorretagem()
    ready.read(file_name)





test_import_corretagem()
