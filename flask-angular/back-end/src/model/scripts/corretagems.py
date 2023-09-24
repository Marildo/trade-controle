# @author Marildo Cesar 19/09/2023

class ArquivosCorretagemSQL:
    query_list = '''
SELECT a.*, MIN(n.data_referencia) data_referencia FROM arquivos_corretagem a
LEFT JOIN notas_corretagem n ON n.file_id = a.id
WHERE 1=1 '''
