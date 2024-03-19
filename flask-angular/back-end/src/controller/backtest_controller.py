# @author Marildo Cesar 09/02/2024

import os
import json
import threading
from collections import OrderedDict
from datetime import date, timedelta
import time
from typing import List

from flask import request, make_response, send_file
from marshmallow import fields
from webargs.flaskparser import parser
from webargs import validate

import numpy
import pandas

from src.services import YFinanceService
from src.utils import rest_util
from src.utils.json_util import CustomJsonEncoder

from .ativos_controller import AtivoController


class BacktestController:

    @classmethod
    def run(cls, export_csv: bool):
        input_schema = {
            'ativos': fields.Str(required=True),
            'start_date': fields.Date(required=True),
            'end_date': fields.Date(required=False),
            'var_percent': fields.Float(required=True),
            'stop': fields.Float(required=True),
            'capital': fields.Float(required=True),
            'costs': fields.Float(required=True),
            'expect_mat': fields.Float(required=True),
            'volume_min': fields.Float(required=False),
            'moving_average': fields.Integer(required=False),
            'timeframe': fields.Str(required=False),
            'strategy': fields.Integer(required=False, validate=validate.OneOf([1, 2])),
        }

        location = rest_util.get_location(request)
        args = dict(parser.parse(input_schema, request, location=location))
        args.setdefault('end_date', date.today() - timedelta(days=1))
        args.setdefault('volume_min', 1_500_000)
        args.setdefault('strategy', 1)
        args.setdefault('timeframe', '1d')
        args.setdefault('moving_average', '21')

        print(args)

        ativos = str(args['ativos'])
        if ativos.__contains__(';'):
            ativos = ativos.split(';')
        elif ativos.__contains__(','):
            ativos = ativos.split(',')
        else:
            ativos = ativos.split('\n')

        var_percent = args['var_percent']
        start = args['start_date']
        end = args['end_date']
        stop = args['stop']
        custos = args['costs']
        capital = args['capital']
        expect_mat = args['expect_mat']
        volume_min = args['volume_min']
        strategy = int(args['strategy'])
        timeframe = args['timeframe']  # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        moving_average = args['moving_average']

        at_ctl = AtivoController()
        data = []
        i = 0
        for ativo in ativos:
            i += 1
            ativo = ativo.strip()
            if not ativo:
                continue
            at = at_ctl.find_by_or_save(ativo)
            if not at:
                continue
            print(ativo, f'{i}/{len(ativos)}', end='')

            historico = YFinanceService().get_historic(ativo, start, end, timeframe)
            if strategy == 1:
                result = cls.faca_caindo(historico, var_percent, stop, capital, custos)
            else:
                result = cls.maxima_minimas(historico, stop, capital, custos, moving_average)

            expect_mat_test = expect_mat == 0 or expect_mat <= result['expectativa_matematica']
            valume_min_test = volume_min == 0 or volume_min <= result['media_volume']
            if expect_mat_test and valume_min_test:
                result['ativo'] = ativo
                data.append(result)

        data.sort(key=lambda x: x['expectativa_matematica'], reverse=True)

        if export_csv:
            for d in data:
                del d['trades']

            df = pandas.DataFrame.from_dict(data)
            csv_file = f'/backtest_varPercent{var_percent}_stop{stop}_{start}_{end}.csv'
            df.to_csv(csv_file, index=False)

            def delete_file():
                time.sleep(5)
                os.remove(csv_file)

            t = threading.Thread(target=delete_file)
            t.start()

            return send_file(csv_file, as_attachment=True)
        else:
            ativos = [i['ativo'] for i in data]
            content = OrderedDict()
            content['success'] = True
            content['data'] = {
                'ativos': ativos,
                'items': data
            }

            json_resp = json.dumps(content, cls=CustomJsonEncoder, ensure_ascii=False)
            response = make_response(json_resp, 200)
            response.headers['Content-Type'] = 'application/json'
            return response

    @classmethod
    def faca_caindo(cls, historico, down_percent: float, stop: float, capital: float, custos: float):
        trades = []
        percent = ()
        last_trade = None
        print('Loaded hist... ', end='processing... ')
        length = len(historico)
        for i in range(1, length):  # começar na segunda linha
            abertura = round(historico['Open'].iloc[i], 2)
            minima = round(historico['Low'].iloc[i], 2)
            fechamento = round(historico['Close'].iloc[i], 2)
            volume = historico['Volume'].iloc[i]
            data = historico.index[i]
            day = date(year=data.year, month=data.month, day=data.day)
            fechamento_anterior = round(historico['Close'].iloc[i - 1], 2)
            start_mov = abertura if abertura > fechamento_anterior else fechamento_anterior

            variacao_x = round(fechamento_anterior * (100 - abs(down_percent)) * 0.01, 2)
            if minima <= variacao_x:
                last_trade = day
                preco_compra = variacao_x if abertura > variacao_x else abertura
                preco_stop = preco_compra * ((100 - stop) * 0.01) if stop != 0 else 0
                stoped = fechamento < preco_stop or minima < preco_stop
                preco_venda = preco_stop if stoped else fechamento

                resultado = round((preco_venda - preco_compra) / preco_compra * 100, 2)
                res_value = round(capital * (resultado * 0.01), 2)
                ir = res_value * 0.01 if res_value > 0 else 0
                resultado_liquido = res_value - custos - ir
                capital += res_value - custos - ir
                trades.append({
                    'preco_venda': preco_venda,
                    'preco_compra': preco_compra,
                    'resultado': resultado_liquido,
                    'resultado_percentual': resultado,
                    'date': day,
                    'fechamento_anterior': fechamento_anterior,
                    'abertura': abertura,
                    'minima': minima,
                    'start_mov': start_mov,
                    'stoped': stoped,
                    'capital_acumulado': round(capital, 2),
                    'volume': volume
                })
                p = int((i + 1) * 100 / length)
                if p % 10 == 0 and p not in percent:
                    print(f' {p}%', end='')
                    percent += (p,)

        resultados = [i['resultado'] for i in trades]

        ganhos = [r for r in resultados if r > 0]
        perdas = [r for r in resultados if r <= 0]

        media_ganhos = round(sum(ganhos) / len(ganhos) if ganhos else 0, 2)
        media_perdas = round(sum(perdas) / len(perdas) if perdas else 0, 2)
        media_resultados = round(sum(resultados) / len(resultados) if resultados else 0, 2)
        media_volume = float(numpy.mean([i['volume'] for i in trades])) if trades else 0

        percentual_ganho = round((len(ganhos) / len(resultados)) * 100 if resultados else 0, 2)
        percentual_perda = round((len(perdas) / len(resultados)) * 100 if resultados else 0, 2)

        seq_ganhos = 0
        seq_perdas = 0
        total_stops = 0

        print(' total_trades: ', len(trades))

        g = 0
        p = 0
        for i in trades:
            if i['resultado'] > 0:
                g += 1
                p = 0
            else:
                p += 1
                g = 0
                if i['stoped']:
                    total_stops += 1

            if p > seq_perdas:
                seq_perdas = p

            if g > seq_ganhos:
                seq_ganhos = g

        result = {
            'ativo': '',
            'total_trades': len(trades),
            'trades_gain': len(ganhos),
            'trades_loss': len(perdas),
            'total_stops': total_stops,
            'expectativa_matematica': media_resultados,
            'percentual_ganho': percentual_ganho,
            'percentual_perda': percentual_perda,
            'media_ganhos': media_ganhos,
            'media_perdas': media_perdas,
            'media_volume': media_volume,
            'sequencia_perdas': seq_perdas,
            'sequencia_ganhos': seq_ganhos,
            'capital_final': round(capital, 2),
            'last_trade': last_trade,
            'trades': trades,
        }

        return result

    @classmethod
    def maxima_minimas(cls, historico, stop: float, capital: float, custos: float, moving_average):
        trades = []
        percent = ()
        last_trade = None
        print('Loaded hist... ', end='processing... ')
        length = len(historico)
        closes = ()
        is_bought = False
        is_sold = False
        buy_at = None
        sell_at = None

        for i in range(1, length):  # começar na segunda linha
            high_last = round(historico['High'].iloc[i], 2)
            high_previous = round(historico['High'].iloc[i - 1], 2)

            low_last = round(historico['Low'].iloc[i], 2)
            low_previous = round(historico['Low'].iloc[i - 1], 2)

            df = pandas.DataFrame(closes, columns=['closes'])
            avgs = df['closes'].rolling(window=moving_average).mean()
            avg_last = avgs.iloc[-1]
            avg_previous = avgs.iloc[-2] if len(avgs) > 1 else avg_last



            if not is_sold and not is_bought:
                # to buy
                if high_last < avg_last < avg_previous:
                    buy_at = high_previous

            if buy_at and high_last > buy_at:
                preco_compra = buy_at
                sell_at = False
                is_bought = True

            abertura = 0
            down_percent = 0

            volume = historico['Volume'].iloc[i]
            data = historico.index[i - 1]
            day = date(year=data.year, month=data.month, day=data.day)
            fechamento_anterior = round(historico['Close'].iloc[i - 1], 2)
            start_mov = abertura if abertura > fechamento_anterior else fechamento_anterior

            variacao_x = round(fechamento_anterior * (100 - abs(down_percent)) * 0.01, 2)
            if minima <= variacao_x:
                last_trade = day
                preco_compra = variacao_x if abertura > variacao_x else abertura
                preco_stop = preco_compra * ((100 - stop) * 0.01) if stop != 0 else 0
                stoped = fechamento < preco_stop or minima < preco_stop
                preco_venda = preco_stop if stoped else fechamento

                resultado = round((preco_venda - preco_compra) / preco_compra * 100, 2)
                res_value = round(capital * (resultado * 0.01), 2)
                ir = res_value * 0.01 if res_value > 0 else 0
                resultado_liquido = res_value - custos - ir
                capital += res_value - custos - ir
                trades.append({
                    'preco_venda': preco_venda,
                    'preco_compra': preco_compra,
                    'resultado': resultado_liquido,
                    'resultado_percentual': resultado,
                    'date': day,
                    'fechamento_anterior': fechamento_anterior,
                    'abertura': abertura,
                    'minima': minima,
                    'start_mov': start_mov,
                    'stoped': stoped,
                    'capital_acumulado': round(capital, 2),
                    'volume': volume
                })
                p = int((i + 1) * 100 / length)
                if p % 10 == 0 and p not in percent:
                    print(f' {p}%', end='')
                    percent += (p,)

        resultados = [i['resultado'] for i in trades]

        ganhos = [r for r in resultados if r > 0]
        perdas = [r for r in resultados if r <= 0]

        media_ganhos = round(sum(ganhos) / len(ganhos) if ganhos else 0, 2)
        media_perdas = round(sum(perdas) / len(perdas) if perdas else 0, 2)
        media_resultados = round(sum(resultados) / len(resultados) if resultados else 0, 2)
        media_volume = float(numpy.mean([i['volume'] for i in trades])) if trades else 0

        percentual_ganho = round((len(ganhos) / len(resultados)) * 100 if resultados else 0, 2)
        percentual_perda = round((len(perdas) / len(resultados)) * 100 if resultados else 0, 2)

        seq_ganhos = 0
        seq_perdas = 0
        total_stops = 0

        print(' total_trades: ', len(trades))

        g = 0
        p = 0
        for i in trades:
            if i['resultado'] > 0:
                g += 1
                p = 0
            else:
                p += 1
                g = 0
                if i['stoped']:
                    total_stops += 1

            if p > seq_perdas:
                seq_perdas = p

            if g > seq_ganhos:
                seq_ganhos = g

        result = {
            'ativo': '',
            'total_trades': len(trades),
            'trades_gain': len(ganhos),
            'trades_loss': len(perdas),
            'total_stops': total_stops,
            'expectativa_matematica': media_resultados,
            'percentual_ganho': percentual_ganho,
            'percentual_perda': percentual_perda,
            'media_ganhos': media_ganhos,
            'media_perdas': media_perdas,
            'media_volume': media_volume,
            'sequencia_perdas': seq_perdas,
            'sequencia_ganhos': seq_ganhos,
            'capital_final': round(capital, 2),
            'last_trade': last_trade,
            'trades': trades,
        }

        return result

    # @staticmethod
    # def calcula_media_movel(medias, window):
    #     media_movel_lista = []
    #     for i in range(len(medias) - window + 1):
    #         media_movel = sum(medias[i:i + window]) / window
    #         media_movel_lista.append(media_movel)
    #     return media_movel_lista
