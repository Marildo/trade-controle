# @author Marildo Cesar 23/10/2023

class CarteiraSQL:
    totalize_saldo_caixa = '''
WITH total AS (
SELECT carteira_id, SUM(valor) total
FROM historicos
GROUP BY carteira_id
)
UPDATE total JOIN carteiras c
ON c.id = total.carteira_id
SET saldo_caixa = total.total
'''