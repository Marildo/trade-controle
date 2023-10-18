# @author Marildo Cesar 21/09/2023


class DividendosSql:
    load_ativos = '''
    SELECT o.ativo_id, a.codigo, MIN(o.data_compra) dt_start, MAX(o.data_venda) dt_end
    FROM operacoes o
    JOIN ativos a ON a.id = o.ativo_id
    LEFT JOIN carteiras ct ON ct.id = o.carteira_id
    WHERE o.daytrade=0 AND o.compra_venda='COMPRA' 
    AND (a.tipo_investimento = "FIIS" OR ct.dividendos = 1 OR ct.buyhold = 1)
    GROUP BY a.id
    '''

    get_qtd = '''
    WITH
	compras AS (
    SELECT COALESCE(SUM(qtd_compra),0) qtd_compras
    FROM operacoes o
    WHERE daytrade=0 AND compra_venda='COMPRA'  AND  o.ativo_id = :ativo_id AND o.data_compra <= :data_ref 
   ),
	vendas AS (
    SELECT COALESCE(SUM(qtd_venda),0) qtd_vendas
    FROM operacoes o
    WHERE daytrade=0 AND compra_venda='COMPRA'  AND o.ativo_id = :ativo_id AND o.data_venda <= :data_ref 
   )   
   SELECT qtd_compras - qtd_vendas qtd FROM compras, vendas
    '''
