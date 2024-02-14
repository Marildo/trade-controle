# @author Marildo Cesar 19/09/2023


class OperacoesSql:
    query_detail = '''
    SELECT
        o.*,
        a.codigo ativo,
        c.nome carteira,
        nc.comprovante nota_compra,
        nv.comprovante nota_venda,
        s.nome setup
    FROM
        operacoes o
        JOIN ativos a ON a.id = o.ativo_id
        LEFT JOIN notas_corretagem nc ON nc.id = o.nota_compra_id
        LEFT JOIN notas_corretagem nv ON nv.id = o.nota_venda_id
        LEFT JOIN carteiras c ON c.id = o.carteira_id
        LEFT JOIN setups s on s.id = o.setup_id
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

    query_daytrade_operations = '''
    SELECT 
        data_encerramento data ,a.codigo, ROUND(SUM(o.resultado -o.irpf - o.custos),2) total
        FROM operacoes o
        JOIN ativos a ON a.id = o.ativo_id
    WHERE data_encerramento >= :start_date AND daytrade=1
    GROUP BY data_encerramento, a.codigo ORDER BY data_encerramento
    '''

    query_summary_total = '''
    SELECT * FROM 
    (SELECT SUM(o.resultado - o.irpf - o.custos) anual 
        FROM operacoes o WHERE data_encerramento >= CONCAT(YEAR(CURRENT_DATE()), '-01-01') AND daytrade = :daytrade ) AS a,
    (SELECT SUM(o.resultado - o.irpf - o.custos) mensal
        FROM operacoes o WHERE data_encerramento >= DATE_FORMAT(CURDATE(), '%Y-%m-01') AND daytrade = :daytrade) AS b,
    (SELECT SUM(o.resultado - o.irpf - o.custos) semanal 
        FROM operacoes o WHERE data_encerramento >= 
        DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) DAY) AND daytrade= :daytrade) AS c,
    (SELECT SUM(o.resultado - o.irpf - o.custos) acumulado 
        FROM operacoes o WHERE daytrade = :daytrade) AS d '''

    query_summary_quarter_daytrade = '''
    WITH QUERY01 AS(
    SELECT 
    	YEAR(o.data_encerramento) ano, 
    	MONTH(o.data_encerramento) mes, 
    	MAX(data_encerramento) encerramento,  
    	SUM(o.resultado - o.irpf - o.custos) AS resultado	
    FROM
     operacoes o
    WHERE o.encerrada=1 AND daytrade=1
    GROUP BY 1,2
    ORDER BY encerramento DESC
    ),

    QUERY02 AS (
    SELECT 
    	encerramento,  
    	resultado,ano,
     	CASE 
    		WHEN mes <= 3 THEN 1
    		WHEN mes BETWEEN 4 AND 6 THEN 2
    		WHEN mes BETWEEN 7 AND 9 THEN 3
    		ELSE 4
    	END 'trimestre'	
    FROM QUERY01
    )

    SELECT  
        ROUND(SUM(resultado),2) total, ano, trimestre,MAX(encerramento) encerramento, 
        CONCAT(LPAD( trimestre * 3,2,'0'),'/',ano) data_group
    FROM QUERY02
    GROUP BY ano, trimestre 
    ORDER BY encerramento '''

    query_statistics_daytrade = '''
    WITH 
        QUERY01 AS (
            SELECT 
            resultado gross,
            custos + irpf costs,
            resultado - (custos + irpf) net
            FROM operacoes o
            WHERE data_encerramento >= :start_date AND daytrade=1)

            ,SUMMARY_TOTAL AS(
             SELECT 
                ROUND(SUM(net),2) net_total,
                ROUND(SUM(gross),2) gross_total,
                ROUND(SUM(costs),2) costs_total,
                ROUND(AVG(gross),2) avg_total,
                COUNT(1) total_trades
             FROM  QUERY01	)

            ,SUMMARY_GAIN AS(
            SELECT 
              COUNT(1) count_gain,	 
              COALESCE(MAX(gross),0) biggest_gain,
              ROUND(COALESCE(AVG(gross),0),2) avg_gain
            FROM QUERY01 WHERE gross > 0)

            ,SUMMARY_LOSS AS(
            SELECT 
              COUNT(1) count_loss,	  
              COALESCE(MIN(gross),0) biggest_loss,
              ROUND(COALESCE(AVG(gross),0),2) avg_loss
            FROM QUERY01 WHERE gross <= 0)

    SELECT
        SUMMARY_TOTAL.*,
        SUMMARY_GAIN.*,
        SUMMARY_LOSS.*,
        ROUND(count_gain * 100 / total_trades,2) perc_gain
        FROM SUMMARY_GAIN,SUMMARY_LOSS,SUMMARY_TOTAL 
        '''

    # TODO -  remover
    query_compras_without_historic = """
    SELECT o.id, o.data_compra,o.qtd_compra, o.pm_compra,o.resultado, o.custos, o.irpf, o.daytrade, 
        o.encerrada, o.carteira_id, o.compra_venda, a.codigo
        FROM operacoes o
        JOIN ativos a ON a.id = o.ativo_id
        LEFT JOIN historicos h ON h.compra_id = o.id
        WHERE h.compra_id IS NULL
    """

    # TODO -  remover
    query_vendas_without_historic = """
    SELECT o.id, o.data_venda, o.qtd_venda, o.pm_venda ,o.resultado, o.custos, o.irpf, o.daytrade, 
        o.encerrada, o.carteira_id, o.compra_venda, a.codigo
        FROM operacoes o
        JOIN ativos a ON a.id = o.ativo_id
        LEFT JOIN historicos h ON h.venda_id = o.id
        WHERE h.venda_id IS NULL
    """
