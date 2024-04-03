# @author Marildo Cesar 19/09/2023

class ArquivosCorretagemSQL:
    query_list = '''
    SELECT a.*, MIN(n.data_referencia) data_referencia FROM arquivos_corretagem a
        LEFT JOIN notas_corretagem n ON n.file_id = a.id
    WHERE 1=1 
    '''

    get_operacoes_for_delete_by_file_id = '''
        SELECT 
            nc.file_id, o.id op_id, o.compra_hist_id, o.venda_hist_id 
        FROM  arquivos_corretagem ac 
            JOIN notas_corretagem nc on nc.file_id  = ac.id
            JOIN operacoes o on o.nota_compra_id  = nc.id  or o.nota_venda_id = nc.id
        WHERE ac.id = :file_id
    '''

    delete_operacoes = '''
        DELETE operacoes WHERE id = :op_id;
        DELETE historicos WHERE h.id = :compra_hist_id;
        DELETE historicos WHERE h.id = :venda_hist_id;
        DELETE notas_corretagem WHERE file_id = :file_id;
    '''
