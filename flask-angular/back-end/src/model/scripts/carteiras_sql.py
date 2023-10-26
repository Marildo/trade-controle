# @author Marildo Cesar 23/10/2023

class CarteiraSQL:
    totalize_saldo_caixa = """
WITH total AS (
    SELECT carteira_id, SUM(valor) total
    FROM historicos
    GROUP BY carteira_id
    )
    UPDATE total JOIN carteiras c
    ON c.id = total.carteira_id
    SET saldo_caixa = total.total
"""

    totalize_saldo_ativos = """
WITH
    compras AS (
        SELECT ativo_id, carteira_id, COALESCE(SUM(qtd_compra),0) qtd_compras
        FROM operacoes o
        WHERE daytrade=0 AND compra_venda='COMPRA'
        GROUP BY ativo_id, carteira_id   
    ),
    vendas AS (
        SELECT ativo_id, carteira_id, COALESCE(SUM(qtd_venda),0) qtd_vendas
        FROM operacoes o
        WHERE daytrade=0 AND compra_venda='COMPRA'  
        GROUP BY ativo_id, carteira_id
   ),   
   saldo_qtd AS (
        SELECT 
        COALESCE(c.ativo_id,v.ativo_id) ativo_id,
        COALESCE(c.carteira_id,v.carteira_id) carteira_id,
        COALESCE(c.qtd_compras,0) - COALESCE(v.qtd_vendas,0) qtd
        FROM compras c
        LEFT JOIN vendas v ON c.ativo_id = v.ativo_id AND c.carteira_id = v.carteira_id
    ),
    total AS (      
        SELECT  s.carteira_id, sum(qtd * a.cotacao) total FROM saldo_qtd s
        JOIN ativos a ON a.id = s.ativo_id
        WHERE qtd > 0 GROUP BY carteira_id
    )
       
    UPDATE carteiras c 
    JOIN total ON total.carteira_id = c.id
    SET c.saldo_ativos = total.total
"""
