# @author Marildo Cesar 19/09/2023

class ArquivosCorretagemSQL:
    query_list = '''
    SELECT a.*, MIN(n.data_referencia) data_referencia FROM arquivos_corretagem a
        LEFT JOIN notas_corretagem n ON n.file_id = a.id
    WHERE 1=1 
    '''

    delete_operacoes_from_file_id = '''
        WITH 
         tmp AS(
            SELECT 
                nc.file_id 
                ,o.id op_id ,o.compra_hist_id ,o.venda_hist_id 
            FROM  arquivos_corretagem ac 
            JOIN notas_corretagem nc on nc.file_id  = ac.id
            JOIN operacoes o on o.nota_compra_id  = nc.id  or o.nota_venda_id = nc.id
            WHERE ac.id=296 and o.daytrade = 1
        )
        
        DELETE FROM o USING operacoes o JOIN tmp on tmp.op_id = o.id;
        DELETE FROM h USING historicos h JOIN tmp on tmp.compra_hist_id = h.id;
        DELETE FROM h USING historicos h JOIN tmp on tmp.venda_hist_id = h.id;
        DELETE FROM h USING notas_corretagem nc JOIN tmp on tmp.file_id = nc.file_id;
    '''
