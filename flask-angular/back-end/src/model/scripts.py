"""
 @author Marildo Cesar 30/05/2023
"""


class OperacoesSql:
    query_detail = '''
SELECT
    o.*,
    a.codigo ativo,
    c.nome carteira,
    nc.comprovante nota_compra,
    nv.comprovante nota_venda
FROM
    operacoes o
    JOIN ativos a ON a.id = o.ativo_id
    LEFT JOIN notas_corretagem nc ON nc.id = o.nota_compra_id
    LEFT JOIN notas_corretagem nv ON nv.id = o.nota_venda_id
    LEFT JOIN carteiras c ON c.id = o.carteira_id
    WHERE 1=1
'''

    query_summary = '''
SELECT
    a.codigo ativo,
    a.cotacao,
    a.id ativo_id,
    IF(o.compra_venda = 'COMPRA', 'Comprado', 'Vendido') tipo,
    IF(o.compra_venda = 'COMPRA', MIN(data_compra),MIN(data_venda)) abertura, 
    c.nome carteira,
    SUM(qtd_compra - qtd_venda) qtd,
    SUM(
        IF(
            o.compra_venda = 'COMPRA',
            a.cotacao * qtd_compra - pm_compra * qtd_compra,
            pm_venda * qtd_venda - a.cotacao * qtd_venda
        )
    ) resultado,
    IF(o.compra_venda = 'COMPRA', 
      SUM(qtd_compra * pm_compra) / SUM(qtd_compra),
      SUM(qtd_venda * pm_venda) / SUM(qtd_venda)
   ) pm_medio
FROM
    operacoes o
    JOIN ativos a ON a.id = o.ativo_id
    LEFT JOIN carteiras c ON c.id = o.carteira_id
    WHERE o.encerrada=0 
'''

    query_daytrade_month = '''
SELECT 
    DATE_FORMAT(data_encerramento,'%d/%m') data ,a.codigo, ROUND(SUM(o.resultado -o.irpf - o.custos),2) total
    FROM operacoes o
    JOIN ativos a ON a.id = o.ativo_id
WHERE data_encerramento >= DATE_FORMAT(CURDATE(), '%Y-%m-01') AND daytrade=1
GROUP BY data_encerramento, a.codigo
'''

    query_summary_daytrade = '''
SELECT * FROM 
(SELECT SUM(o.resultado - o.irpf - o.custos) anual 
    FROM operacoes o WHERE data_encerramento >= CONCAT(YEAR(CURRENT_DATE()), '-01-01') AND daytrade=1 ) AS a,
(SELECT SUM(o.resultado - o.irpf - o.custos) mensal
    FROM operacoes o WHERE data_encerramento >= DATE_FORMAT(CURDATE(), '%Y-%m-01') AND daytrade=1) AS b,
(SELECT SUM(o.resultado - o.irpf - o.custos) semanal 
    FROM operacoes o WHERE data_encerramento >= DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) DAY) AND daytrade=1) AS c,
(SELECT SUM(o.resultado - o.irpf - o.custos) acumulado 
    FROM operacoes o WHERE daytrade=1) AS d
'''
