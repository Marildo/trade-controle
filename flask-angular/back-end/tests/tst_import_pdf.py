"""
 @author Marildo Cesar 23/04/2023
"""


def import_corretagem():
    from services.corretagem.read_pdf_file import ReadPDFCorretagem

    file_name: str = "C:\\Users\\maril\\Downloads\\nota-futuro-2024_05_14.pdf"
    # file_name: str = "nota-futuro-2023_04_26.pdf"

    ready = ReadPDFCorretagem()
    ready.read(file_name)
    for item in ready.notas():
        for o in item.operacoes:
            print(o)

import_corretagem()
