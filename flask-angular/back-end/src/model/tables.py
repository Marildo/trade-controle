"""
 @author Marildo Cesar 24/04/2023
"""

from typing import List, Dict
from datetime import date

from sqlalchemy import (Column, Index, INTEGER, VARCHAR, CHAR, FLOAT, DATE, DATETIME, TIMESTAMP, BOOLEAN, Enum,
                        ForeignKey, text, func)
from sqlalchemy.orm import relationship

from .init_db import db_connection, Base
from .enums import TipoInvestimento, TipoNota, TipoCarteira, CompraVenda, NotaStatusProcess

from .scripts import OperacoesSql, ArquivosCorretagemSQL


class BaseTable(Base):
    __abstract__ = True

    def save(self):
        with db_connection as conn:
            conn.session.add(self)
            conn.session.commit()

    def update(self):
        with db_connection as conn:
            conn.session.merge(self)
            conn.session.commit()

    def read_by_id(self, _id: int):
        with db_connection as conn:
            _class = type(self)
            query = (conn.session.query(_class)
                     .filter(_class.id == _id)
                     )
            return query.first()

    def read_by_params(self, params: Dict) -> List:
        _class = type(self)

        filters = []
        if params:
            columns = _class.__table__.columns
            for k, v in params.items():
                translasted = self.translate_query(field=k, value=v)
                if translasted is not None:
                    filters.append(translasted)
                elif k in columns:
                    filters.append(columns[k] == v)

        with db_connection as conn:
            query = (conn.session.query(_class)
                     .filter(*filters)
                     )
            return query.all()

    def translate_query(self, field: str, value: str):
        return None


class Setor(BaseTable):
    __tablename__ = 'setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    subsetores = relationship("SubSetor", uselist=True, backref='setores')

    def __str__(self) -> str:
        return f'{self.id} - {self.nome}'


class SubSetor(BaseTable):
    __tablename__ = 'sub_setores'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))


class Segmento(BaseTable):
    __tablename__ = 'segmentos'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(60))


class Ativo(BaseTable):
    __tablename__ = 'ativos'
    id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER, default=0)
    codigo = Column(CHAR(6))
    nome = Column(VARCHAR(60))
    descricao = Column(VARCHAR(90))
    cotacao = Column(FLOAT(precision=3))
    variacao = Column(FLOAT(precision=3))
    tipo_ativo = Column(VARCHAR(6), nullable=True)
    tipo_investimento = Column(Enum(TipoInvestimento))
    update_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    setor_id = Column(INTEGER, ForeignKey('setores.id'))
    setor = relationship("Setor")
    segmento_id = Column(INTEGER, ForeignKey('segmentos.id'))
    segmento = relationship("Segmento")

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @staticmethod
    def find_by_codigo(codigo: str):
        with db_connection as conn:
            query = conn.session.query(Ativo).filter(Ativo.codigo == codigo)
            return query.first()

    @staticmethod
    def find_like_name(nome: str):
        with db_connection as conn:
            query = conn.session.query(Ativo).filter(Ativo.nome.ilike(f'%{nome.strip()}%'))
            return query.all()


class Carteira(BaseTable):
    __tablename__ = 'carteiras'
    id = Column(INTEGER, primary_key=True)
    nome = Column(VARCHAR(40))
    saldo_ativos = Column(FLOAT, default=0)
    saldo_caixa = Column(FLOAT, default=0)
    tipo = Column(Enum(TipoCarteira))
    daytrade = Column(BOOLEAN, default=False, nullable=False)
    dividendos = Column(BOOLEAN, default=False, nullable=False)
    buyhold = Column(BOOLEAN, default=False, nullable=False)
    descricao = Column(VARCHAR(120))


class FileCorretagem(BaseTable):
    __tablename__ = 'arquivos_corretagem'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(120))
    tipo = Column(Enum(TipoNota))
    status = Column(Enum(NotaStatusProcess))
    data_upload = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))
    data_processamento = Column(DATETIME)
    notas = relationship("NotaCorretagem", uselist=True, backref='arquivos_corretagem')
    __table_args__ = (Index('tipo', 'name', unique=True),)

    def is_exists(self) -> bool:
        with db_connection as conn:
            query = (conn.session.query(FileCorretagem)
                     .filter(FileCorretagem.name == self.name,
                             # FileCorretagem.status != NotaStatusProcess.ERROR
                             )
                     )
            return query.first()

    def translate_query(self, field: str, value: str):
        map_fields = {
            'start_processamento': eval(f'{FileCorretagem.data_processamento} >= "{value} 00:00:00"'),
            'end_processamento': eval(f'{FileCorretagem.data_processamento} <= "{value} 23:59:59"')
        }
        if field in map_fields:
            return map_fields[field]

        return None

    @staticmethod
    def list_arquivos(params: Dict) -> List:
        # TODO pode passar isso para um metodos generico

        if 'tipo' in params:
            params['tipo'] = TipoNota(params['tipo']).name

        filters_map = {key: value for key, value in params.items() if key not in ['size', 'page', 'orderby']}

        filter_translater = {
            'start_referencia': 'data_referencia >= :start_referencia',
            'end_referencia': 'data_referencia <= :end_referencia',
            'start_processamento': 'data_processamento >= :start_processamento',
            'end_processamento': 'data_processamento <= :end_processamento',
        }

        key_params = []
        for key, value in filters_map.items():
            if key in filter_translater:
                key_params.append(filter_translater[key])
            else:
                key_params.append(f'{key} = :{key}')

        where = f' AND {" AND ".join(key_params)}' if key_params else ''
        order_group_by = ' GROUP BY a.id ORDER BY data_referencia'
        sql = text(ArquivosCorretagemSQL.query_list + where + order_group_by)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, filters_map)
            return query.fetchall()


class NotaCorretagem(BaseTable):
    __tablename__ = 'notas_corretagem'
    id = Column(INTEGER, primary_key=True)
    comprovante = Column(INTEGER)
    data_referencia = Column(DATE)
    finalizada = Column(BOOLEAN, default=False)
    file_id = Column(INTEGER, ForeignKey('arquivos_corretagem.id'))
    Index('idx_comprovante', comprovante, data_referencia, unique=True)

    def __str__(self):
        return f'Data: {self.data_referencia} - Comprovante: {self.comprovante} '

    def find_self(self):
        return self.read_by_params(dict(comprovante=self.comprovante, data_referencia=self.data_referencia))

    @staticmethod
    def get_last_date_processed():
        with db_connection as conn:
            query = conn.session.query(func.max(NotaCorretagem.data_referencia))
            return query.one()


class Operacao(BaseTable):
    __tablename__ = 'operacoes'

    id = Column(INTEGER, primary_key=True)
    data_compra = Column(DATE, nullable=True)
    data_venda = Column(DATE, nullable=True)
    pm_compra = Column(FLOAT(precision=2), default=0)
    pm_venda = Column(FLOAT(precision=2), default=0)
    qtd_compra = Column(FLOAT(precision=2), default=0)
    qtd_venda = Column(FLOAT(precision=2), default=0)
    custos = Column(FLOAT(precision=4), default=0)
    irpf = Column(FLOAT(precision=4), default=0)
    resultado = Column(FLOAT(precision=4), default=0)
    daytrade = Column(BOOLEAN, default=False, nullable=False)
    encerrada = Column(BOOLEAN, default=False, nullable=False)
    data_encerramento = Column(DATE, nullable=True)
    compra_venda = Column(Enum(CompraVenda))
    ativo_id = Column(INTEGER, ForeignKey('ativos.id'))
    ativo = relationship("Ativo")
    carteira_id = Column(INTEGER, ForeignKey('carteiras.id'))
    carteira = relationship("Carteira")
    nota_compra_id = Column(INTEGER, ForeignKey('notas_corretagem.id'))
    nota_compra = relationship("NotaCorretagem", foreign_keys=[nota_compra_id], lazy=True)
    nota_venda_id = Column(INTEGER, ForeignKey('notas_corretagem.id'))
    nota_venda = relationship("NotaCorretagem", foreign_keys=[nota_venda_id], lazy=True)

    def __init__(self):
        self.qtd_compra = 0.0
        self.qtd_venda = 0.0
        self.pm_venda = 0.0
        self.pm_compra = 0.0
        self.custos = 0.0
        self.irpf = 0.0

    @property
    def qtd_aberta(self) -> float:
        return self.qtd_compra - self.qtd_venda

    def calc_resultado(self) -> float:
        if self.encerrada:
            value = (self.qtd_venda * self.pm_venda) - (self.qtd_compra * self.pm_compra)
        else:
            if self.compra_venda == CompraVenda.COMPRA:
                value = (self.ativo.cotacao - self.pm_compra) * self.qtd_compra
            else:
                value = (self.pm_venda - self.ativo.cotacao) * self.qtd_venda

        if self.ativo_id == 800000:
            value = value / 5
        elif self.ativo_id == 900000:
            value = value * 10
        total_custos = self.irpf + self.custos
        value = value - total_custos
        return value

    @staticmethod
    def find_not_closed(ativo: Ativo, compra_venda: CompraVenda, daytrade: bool) -> List:
        with db_connection as conn:
            filters = [Operacao.compra_venda == compra_venda,
                       Operacao.encerrada == 0,
                       Operacao.daytrade == daytrade]
            query = (conn.session.query(Operacao)
                     .join(Ativo, Operacao.ativo_id == ativo.id)
                     .filter(*filters)).all()

            return query

    @staticmethod
    def find_by_nota(id_nota: int) -> List:
        with db_connection as conn:
            filters = [Operacao.nota_venda_id == id_nota, Operacao.encerrada == 1]
            query = (conn.session.query(Operacao).filter(*filters)).all()

            return query

    @staticmethod
    def fetch_detail(params: Dict) -> List:
        filters_map = {key: value for key, value in params.items() if key not in ['size', 'page', 'orderby']}

        filter_translater = {
            'nota_compra': 'nv.comprovante = :nota_compra',
            'nota_venda': 'nc.comprovante = :nota_venda',
            'nota': 'nv.comprovante = :nota OR nc.comprovante = :nota',
            'file_id': 'nv.file_id = :file_id OR nc.file_id = :file_id',
            'start_encerramento': 'data_encerramento >= :start_encerramento',
            'end_encerramento': 'data_encerramento <= :end_encerramento',
            'start_data_compra': 'data_compra >= :start_data_compra',
            'end_data_compra': 'data_compra <= :end_data_compra',
            'start_data_venda': 'data_venda >= :start_data_venda',
            'end_data_venda': 'data_venda <= :end_data_venda',
            'daytrade': 'o.daytrade = :daytrade',
        }

        key_params = []
        for key, value in filters_map.items():
            if key in filter_translater:
                key_params.append(filter_translater[key])
            else:
                key_params.append(f'{key} = :{key}')

        where = f' AND {" AND ".join(key_params)}' if key_params else ''
        order_by = ' ORDER BY data_encerramento, data_compra, data_venda'

        sql = text(OperacoesSql.query_detail + where + order_by)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, filters_map)
            return query.fetchall()

    @staticmethod
    def fetch_summary(params: Dict) -> List:
        filters_map = {key: value for key, value in params.items() if key not in ['size', 'page', 'orderby']}
        fields_filter = [f'{key} = :{key}' for key in filters_map.keys()]
        where = f' AND {" AND ".join(fields_filter)}' if fields_filter else ''
        group = ' GROUP BY o.ativo_id,o.compra_venda,c.id  ORDER BY abertura'
        sql = text(OperacoesSql.query_summary + where + group)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, filters_map)
            return query.fetchall()

    @staticmethod
    def fetch_summary_total(daytrade: bool):
        sql = text(OperacoesSql.query_summary_total)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, dict(daytrade=daytrade))
            return query.one()

    @staticmethod
    def fetch_summary_quarter_daytrade():
        sql = text(OperacoesSql.query_summary_quarter_daytrade)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql)
            return query.fetchall()

    @staticmethod
    def fetch_daytrade_operations(start_date: date) -> List:
        sql = text(OperacoesSql.query_daytrade_operations)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, {'start_date': start_date})
            return query.fetchall()

    @staticmethod
    def fetch_statistics_daytrade(start_date: date):
        sql = text(OperacoesSql.query_statistics_daytrade)
        with db_connection.engine.begin() as conn:
            query = conn.execute(sql, {'start_date': start_date})
            return query.fetchall()


class Dividendos(BaseTable):
    __tablename__ = 'dividendos'

    id = Column(INTEGER, primary_key=True)
    data_com = Column(DATE, nullable=True)
    data_pgto = Column(DATE, nullable=True)
    data_ref = Column(DATE, nullable=True)
    qtd = Column(FLOAT(precision=2), default=0)
    cotacao = Column(FLOAT(precision=2), default=0)
    valor = Column(FLOAT(precision=2), default=0)
    total = Column(FLOAT(precision=2), default=0)
    div_yield = Column(FLOAT(precision=2), default=0)
    ativo_id = Column(INTEGER, ForeignKey('ativos.id'))
    ativo = relationship("Ativo")
    created_at = Column(TIMESTAMP, onupdate=text('CURRENT_TIMESTAMP'), default=text('CURRENT_TIMESTAMP'))

    @staticmethod
    def all():
        with db_connection as conn:
            query = conn.session.query(Dividendos).order_by(Dividendos.data_pgto)
            return query.all()

    @staticmethod
    def find_by_ativo(ativo_id: int):
        with db_connection as conn:
            query = conn.session.query(Dividendos).filter(Dividendos.ativo_id == ativo_id)
            return query.all()
