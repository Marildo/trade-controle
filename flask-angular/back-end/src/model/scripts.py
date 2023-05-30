"""
 @author Marildo Cesar 30/05/2023
"""


class OperacoesSql:
    read_by_param = '''
SELECT
    o.*,
    a.nome ativo,
    c.nome carteira,
    nc.comprovante nota_compra,
    nv.comprovante nota_venda,
    SUM(
        IF(
            o.encerrada,
            pm_venda * qtd_compra - pm_compra * qtd_compra - custos - irpf,
            IF(
                o.compra_venda = 'COMPRA',
                pm_compra * qtd_compra - a.cotacao * qtd_compra,
                pm_venda * qtd_venda - a.cotacao * qtd_venda
            )
        )
    ) resultado
FROM
    operacoes o
    JOIN ativos a ON a.id = o.ativo_id
    LEFT JOIN notas_corretagem nc ON nc.id = o.nota_compra_id
    LEFT JOIN notas_corretagem nv ON nv.id = o.nota_venda_id
    LEFT JOIN carteiras c ON c.id = o.carteira_id
'''
