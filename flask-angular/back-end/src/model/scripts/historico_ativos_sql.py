# @author Marildo Cesar 01/05/2024
class HistoricoAtivosSQL:
    update = """
        UPDATE invest_controll.historico_ativos
            SET abertura=%(abertura)s, fechamento=%(fechamento)s, maxima=%(maxima)s, minima=%(minima)s
    WHERE data=%(data)s AND ativo_id=%(ativo_id)s;    
    """
