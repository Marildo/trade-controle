# @author Marildo Cesar 01/05/2024
class AtivosSQL:
    update = """
        UPDATE invest_controll.ativos
            SET parent_id=0, codigo='', nome='', descricao='', cotacao=0, variacao=0, maxima=0, minima=0, abertura=0, fechamento=0, tipo_ativo='', tipo_investimento='', update_at=CURRENT_TIMESTAMP, setor_id=0, segmento_id=0
    WHERE id=0;

    """
